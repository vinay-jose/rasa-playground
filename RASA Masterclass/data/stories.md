## hospital search happy path
* greet
  - utter_how_can_i_help
* facility_reqd{"facility":"hospital","location":"trivandrum"}
  - action_facility_search
* thanks
  - utter_goodbye

## hospital and then location
* greet
  - utter_how_can_i_help
* facility_reqd{"facility":"hospital"}
  - utter_ask_location
* inform_location{"location":"trivandrum"}
  - action_facility_search
* thanks
  - utter_goodbye

## location and then hospital
* greet
  - utter_how_can_i_help
* inform_location{"location":"trivandrum"}
  - utter_ask_facility
* facility_reqd{"facility":"hospital"}
  - action_facility_search
* thanks
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
