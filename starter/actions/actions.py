"""Custom actions for the MyTwinAgent (RxTwin) clinical coworker.

Principle (from the Rasa playbook): flows own the *conversation logic*; actions do
the *raw work* and hand results back as slots for the flow to branch on.
"""

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.tickets import (
    load_tickets,
    new_ticket_id,
    normalise_ticket_id,
    save_tickets,
    utc_now,
)


class ActionCreateTicket(Action):
    def name(self) -> Text:
        return "action_create_ticket"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tickets = load_tickets()
        ticket_id = new_ticket_id(tickets)
        tickets[ticket_id] = {
            "summary": tracker.get_slot("issue_summary"),
            "category": tracker.get_slot("issue_category"),
            "priority": tracker.get_slot("issue_priority"),
            "email": tracker.get_slot("contact_email"),
            "pharmacist": tracker.get_slot("user_name"),
            "status": "open",
            "created_at": utc_now(),
        }
        save_tickets(tickets)
        # Update cross-session handoff slots so the next session can resume
        # and confirm to the user which ticket was created.
        dispatcher.utter_message(text=f"Incident {ticket_id} opened.")
        return [
            SlotSet("ticket_id", ticket_id),
            SlotSet("has_active_incident", True),
            SlotSet("last_incident_id", ticket_id),
            SlotSet("last_incident_summary", tickets[ticket_id].get("summary")),
        ]


class ActionLookupTicket(Action):
    def name(self) -> Text:
        return "action_lookup_ticket"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ticket_id = normalise_ticket_id(tracker.get_slot("lookup_ticket_id"))
        ticket = load_tickets().get(ticket_id)
        if not ticket:
            return [
                SlotSet("ticket_found", False),
                SlotSet("lookup_ticket_id", ticket_id),
            ]
        return [
            SlotSet("ticket_found", True),
            SlotSet("lookup_ticket_id", ticket_id),
            SlotSet("ticket_status", ticket.get("status", "open")),
            SlotSet("ticket_summary", ticket.get("summary", "")),
        ]


class ActionGreetTwin(Action):
    """Checks for active open incidents to facilitate cross-session shift resumption."""
    def name(self) -> Text:
        return "action_greet_twin"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tickets = load_tickets()
        # Filter all tickets that have an "open" status to find pending exceptions
        open_tickets = [
            (tid, info)
            for tid, info in tickets.items()
            if info.get("status") == "open"
        ]
        
        if open_tickets:
            # Take the latest open compliance ticket
            latest_tid, latest_info = open_tickets[-1]
            events = [
                SlotSet("has_active_incident", True),
                SlotSet("last_incident_id", latest_tid),
                SlotSet("last_incident_summary", latest_info.get("summary", "Vaccine Fridge Temperature Excursion")),
            ]
            pharmacist = latest_info.get("pharmacist")
            if pharmacist and not tracker.get_slot("user_name"):
                events.append(SlotSet("user_name", pharmacist))
            return events
        
        return [
            SlotSet("has_active_incident", False),
            SlotSet("last_incident_id", None),
            SlotSet("last_incident_summary", None),
        ]


class ActionResolveLatestIncident(Action):
    """Mark the latest open incident resolved (Act 2 demo — quarantine complete)."""

    def name(self) -> Text:
        return "action_resolve_latest_incident"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tickets = load_tickets()
        open_tickets = [
            (tid, info)
            for tid, info in tickets.items()
            if info.get("status") == "open"
        ]
        if not open_tickets:
            dispatcher.utter_message(
                text="I don't see an open incident to update right now."
            )
            return [SlotSet("has_active_incident", False)]

        latest_tid, latest_info = open_tickets[-1]
        tickets[latest_tid]["status"] = "resolved"
        tickets[latest_tid]["resolved_at"] = utc_now()
        save_tickets(tickets)
        return [
            SlotSet("last_incident_id", latest_tid),
            SlotSet("last_incident_summary", latest_info.get("summary", "")),
            SlotSet("has_active_incident", False),
            SlotSet("ticket_id", latest_tid),
        ]
