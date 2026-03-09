import streamlit as st
import pandas as pd
from itertools import combinations

st.set_page_config(page_title="TT Tournament Tracker", page_icon="🏓", layout="wide")

EVENTS = {
    "Men's Singles": {
        "type": "groups_to_round_robin_then_final",
        "group_score_max": 21,
        "next_stage_score_max": 2,
        "final_score_max": 2,
        "groups": {
            "A": [
                {"name": "Mithun R", "team": "Team A"},
                {"name": "Swastik", "team": "Team B"},
                {"name": "Prasanth K", "team": "Team C"},
                {"name": "Ramkrishna Khandelwal", "team": "Team D"},
                {"name": "Rohit Waghmare", "team": "Team C"},
                {"name": "Eric Quadros", "team": "Team B"},
                {"name": "Mohanaprasad", "team": "Team D"},
            ],
            "B": [
                {"name": "Ajay Gautam", "team": "Team A"},
                {"name": "Gaurav Maheshwari", "team": "Team B"},
                {"name": "Karthik G", "team": "Team C"},
                {"name": "Yuvraj Singh", "team": "Team D"},
                {"name": "Abhinav Nimje", "team": "Team C"},
                {"name": "Vishal Gupta", "team": "Team B"},
                {"name": "Sasidhar Reddy", "team": "Team A"},
            ],
            "C": [
                {"name": "Jithin Vinod", "team": "Team A"},
                {"name": "Ashish Goyal", "team": "Team B"},
                {"name": "K Ramnath Shenoy", "team": "Team C"},
                {"name": "Vivek Kumar", "team": "Team D"},
                {"name": "Sohail Akhtar", "team": "Team C"},
                {"name": "Abhinav Jha", "team": "Team B"},
                {"name": "Deva Nikhil Dantuluri", "team": "Team A"},
            ],
            "D": [
                {"name": "Sarthaka", "team": "Team A"},
                {"name": "Pranal Wankhade", "team": "Team B"},
                {"name": "Dandu Madhukar Reddy", "team": "Team C"},
                {"name": "Vishrut Bhatnagar", "team": "Team D"},
                {"name": "Piyush Singh Bora", "team": "Team C"},
                {"name": "Yash Modi", "team": "Team D"},
                {"name": "Chinmay Sandeep Nemade", "team": "Team A"},
            ],
            "E": [
                {"name": "Karthik Shetty", "team": "Team D"},
                {"name": "Ezhilarasan", "team": "Team A"},
                {"name": "Chandan", "team": "Team C"},
                {"name": "Sahil", "team": "Team C"},
                {"name": "Pranava", "team": "Team B"},
                {"name": "Ashish Mathew", "team": "Team D"},
                {"name": "Manjunath", "team": "Team B"},
            ],
        },
    },
    "Men's Doubles": {
        "type": "groups_to_super6_then_final",
        "group_score_max": 21,
        "next_stage_score_max": 2,
        "final_score_max": 2,
        "groups": {
            "A": [
                {"name": "Ajay & Sandeep Y", "team": "Team A"},
                {"name": "Pranava & Swastik", "team": "Team B"},
                {"name": "Prasanth K & Karthik G", "team": "Team C"},
                {"name": "Vishrut Bhatnagar & Ramkrishna", "team": "Team D"},
                {"name": "Deva Nikhil Dantuluri & Mithun R", "team": "Team A"},
                {"name": "Piyush & Chandan", "team": "Team C"},
                {"name": "Lokeshwar & Yash Modi", "team": "Team D"},
            ],
            "B": [
                {"name": "Ezhilarasan & Sharath", "team": "Team A"},
                {"name": "Gaurav & K Ramnath", "team": "Team B"},
                {"name": "Dandu Madhukar Reddy & Rohit Waghmare", "team": "Team C"},
                {"name": "Karthik Shetty & Ashish Mathew", "team": "Team D"},
                {"name": "Jithin & Sarthaka", "team": "Team A"},
                {"name": "Manjunath & Abhinav Jha", "team": "Team B"},
            ],
            "C": [
                {"name": "Chinmay & Sasidhar Reddy", "team": "Team A"},
                {"name": "Pranal & Eric", "team": "Team B"},
                {"name": "Abhinav Nimje & Sahil", "team": "Team C"},
                {"name": "Vivek Kumar & Yuvraj Singh", "team": "Team D"},
                {"name": "Mohanaprasad & Jagannatha", "team": "Team D"},
                {"name": "Samrat & Budumuru Kiran", "team": "Team C"},
            ],
        },
    },
    "Women's Singles": {
        "type": "groups_to_super4",
        "group_score_max": 21,
        "next_stage_score_max": 2,
        "groups": {
            "A": [
                {"name": "Kavya Pathak", "team": "Team A"},
                {"name": "Palak Joshi", "team": "Team B"},
                {"name": "Lavanya Shekar", "team": "Team D"},
                {"name": "Sonam Yadav", "team": "Team C"},
                {"name": "Divya Smitha", "team": "Team B"},
            ],
            "B": [
                {"name": "Jyoti Agarwal", "team": "Team A"},
                {"name": "Khushboo Jain", "team": "Team B"},
                {"name": "Anwesha Mazumdar", "team": "Team A"},
                {"name": "Aishwarya Sharma", "team": "Team B"},
                {"name": "Tulika", "team": "Team C"},
            ],
        },
    },
    "Women's Doubles": {
        "type": "groups_to_final",
        "group_score_max": 21,
        "final_score_max": 2,
        "groups": {
            "A": [
                {"name": "Jyoti & Anwesha", "team": "Team A"},
                {"name": "Divya Smitha & Palak Joshi", "team": "Team B"},
                {"name": "Khushboo Jain & Aishwarya Sharma", "team": "Team B"},
                {"name": "Tulika & Mousumi", "team": "Team C"},
            ],
        },
    },
    "Mixed Doubles": {
        "type": "groups_to_final",
        "group_score_max": 21,
        "final_score_max": 2,
        "groups": {
            "A": [
                {"name": "Deva Nikhil & Jyoti Agarwal", "team": "Team A"},
                {"name": "Jithin & Anwesha", "team": "Team A"},
                {"name": "Khushboo Jain & Eric Quadros", "team": "Team B"},
                {"name": "Divya & Pranava", "team": "Team B"},
                {"name": "Swastik & Palak", "team": "Team B"},
                {"name": "Abhinav Nimje & Tulika", "team": "Team C"},
                {"name": "Karthik G & Mousumi", "team": "Team C"},
                {"name": "Lavanya Shekar & Karthik Shetty", "team": "Team D"},
            ],
        },
    },
}


def all_matches(players):
    return list(combinations(players, 2))


def init_session_state():
    for event_name, event in EVENTS.items():
        event_key = slug(event_name)
        for group_name, players in event["groups"].items():
            names = [p["name"] for p in players]
            for p1, p2 in all_matches(names):
                st.session_state.setdefault(f"{event_key}_group_{group_name}_{p1}_vs_{p2}_p1", None)
                st.session_state.setdefault(f"{event_key}_group_{group_name}_{p1}_vs_{p2}_p2", None)

        if event["type"] == "groups_to_round_robin_then_final":
            group_count = len(event["groups"])
            for i in range(group_count):
                for j in range(i + 1, group_count):
                    st.session_state.setdefault(f"{event_key}_qual_{i}_{j}_p1", None)
                    st.session_state.setdefault(f"{event_key}_qual_{i}_{j}_p2", None)
            st.session_state.setdefault(f"{event_key}_final_p1", None)
            st.session_state.setdefault(f"{event_key}_final_p2", None)

        elif event["type"] == "groups_to_super6_then_final":
            for i in range(6):
                for j in range(i + 1, 6):
                    st.session_state.setdefault(f"{event_key}_super6_{i}_{j}_p1", None)
                    st.session_state.setdefault(f"{event_key}_super6_{i}_{j}_p2", None)
            st.session_state.setdefault(f"{event_key}_final_p1", None)
            st.session_state.setdefault(f"{event_key}_final_p2", None)

        elif event["type"] == "groups_to_super4":
            for i in range(4):
                for j in range(i + 1, 4):
                    st.session_state.setdefault(f"{event_key}_super4_{i}_{j}_p1", None)
                    st.session_state.setdefault(f"{event_key}_super4_{i}_{j}_p2", None)

        elif event["type"] == "groups_to_final":
            st.session_state.setdefault(f"{event_key}_final_p1", None)
            st.session_state.setdefault(f"{event_key}_final_p2", None)


def slug(text):
    return text.lower().replace("'", "").replace(" ", "_")


def compute_group_standings(event_name, group_name, players):
    event_key = slug(event_name)
    rows = {
        p["name"]: {
            "Player": p["name"],
            "Team": p["team"],
            "Played": 0,
            "Wins": 0,
            "Losses": 0,
            "Points For": 0,
            "Points Against": 0,
        }
        for p in players
    }

    for p1, p2 in all_matches([p["name"] for p in players]):
        s1 = st.session_state.get(f"{event_key}_group_{group_name}_{p1}_vs_{p2}_p1")
        s2 = st.session_state.get(f"{event_key}_group_{group_name}_{p1}_vs_{p2}_p2")

        if s1 is None or s2 is None:
            continue

        rows[p1]["Played"] += 1
        rows[p2]["Played"] += 1
        rows[p1]["Points For"] += s1
        rows[p1]["Points Against"] += s2
        rows[p2]["Points For"] += s2
        rows[p2]["Points Against"] += s1

        if s1 > s2:
            rows[p1]["Wins"] += 1
            rows[p2]["Losses"] += 1
        elif s2 > s1:
            rows[p2]["Wins"] += 1
            rows[p1]["Losses"] += 1

    df = pd.DataFrame(rows.values())
    df["Diff"] = df["Points For"] - df["Points Against"]
    df = df.sort_values(
        by=["Wins", "Diff", "Points For", "Player"],
        ascending=[False, False, False, True],
    ).reset_index(drop=True)
    df.index = df.index + 1
    return df


def compute_knockout_round_robin(players, key_prefix):
    rows = {
        p: {
            "Player": p,
            "Played": 0,
            "Wins": 0,
            "Losses": 0,
            "Sets Won": 0,
            "Sets Lost": 0,
        }
        for p in players
    }

    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            s1 = st.session_state.get(f"{key_prefix}_{i}_{j}_p1")
            s2 = st.session_state.get(f"{key_prefix}_{i}_{j}_p2")

            if s1 is None or s2 is None:
                continue
            if (s1, s2) not in [(2, 0), (2, 1), (1, 2), (0, 2)]:
                continue

            p1 = players[i]
            p2 = players[j]
            rows[p1]["Played"] += 1
            rows[p2]["Played"] += 1
            rows[p1]["Sets Won"] += s1
            rows[p1]["Sets Lost"] += s2
            rows[p2]["Sets Won"] += s2
            rows[p2]["Sets Lost"] += s1

            if s1 > s2:
                rows[p1]["Wins"] += 1
                rows[p2]["Losses"] += 1
            else:
                rows[p2]["Wins"] += 1
                rows[p1]["Losses"] += 1

    df = pd.DataFrame(rows.values())
    df["Diff"] = df["Sets Won"] - df["Sets Lost"]
    df = df.sort_values(
        by=["Wins", "Diff", "Sets Won", "Player"],
        ascending=[False, False, False, True],
    ).reset_index(drop=True)
    df.index = df.index + 1
    return df


def render_score_row(label1, label2, key1, key2, max_value):
    c1, c2, c3, c4 = st.columns([3, 1, 1, 3])
    with c1:
        st.markdown(f"**{label1}**")
    with c2:
        st.number_input("", min_value=0, max_value=max_value, step=1, key=key1, label_visibility="collapsed")
    with c3:
        st.number_input(" ", min_value=0, max_value=max_value, step=1, key=key2, label_visibility="collapsed")
    with c4:
        st.markdown(f"<div style='text-align:right'><b>{label2}</b></div>", unsafe_allow_html=True)


def render_group_stage(event_name, event):
    winners = {}
    cols = st.columns(len(event["groups"]))
    for idx, (group_name, players) in enumerate(event["groups"].items()):
        standings = compute_group_standings(event_name, group_name, players)
        winner = standings.iloc[0]["Player"] if len(standings) else f"Winner {group_name}"
        winners[group_name] = winner
        with cols[idx]:
            st.metric(f"Group {group_name} Winner", winner)

    tabs = st.tabs([f"Group {g}" for g in event["groups"].keys()])
    event_key = slug(event_name)

    for idx, (group_name, players) in enumerate(event["groups"].items()):
        with tabs[idx]:
            st.subheader(f"Group {group_name} Matches")
            for p1, p2 in all_matches([p["name"] for p in players]):
                render_score_row(
                    p1,
                    p2,
                    f"{event_key}_group_{group_name}_{p1}_vs_{p2}_p1",
                    f"{event_key}_group_{group_name}_{p1}_vs_{p2}_p2",
                    event["group_score_max"],
                )
            st.subheader(f"Group {group_name} Standings")
            st.dataframe(compute_group_standings(event_name, group_name, players), use_container_width=True)

    return winners


def render_mens_singles(event_name, event):
    winners = render_group_stage(event_name, event)
    event_key = slug(event_name)
    st.subheader("Qualifier Round Robin (Best of 3)")
    qualifier_players = [winners[g] for g in ["A", "B", "C", "D", "E"]]
    for i in range(len(qualifier_players)):
        for j in range(i + 1, len(qualifier_players)):
            render_score_row(
                qualifier_players[i],
                qualifier_players[j],
                f"{event_key}_qual_{i}_{j}_p1",
                f"{event_key}_qual_{i}_{j}_p2",
                event["next_stage_score_max"],
            )

    qualifier_standings = compute_knockout_round_robin(qualifier_players, f"{event_key}_qual")
    st.subheader("Qualifier Standings")
    st.dataframe(qualifier_standings, use_container_width=True)

    st.subheader("Final (Best of 3)")
    finalist_1 = qualifier_standings.iloc[0]["Player"] if len(qualifier_standings) > 0 else "Qualifier Rank 1"
    finalist_2 = qualifier_standings.iloc[1]["Player"] if len(qualifier_standings) > 1 else "Qualifier Rank 2"
    render_score_row(finalist_1, finalist_2, f"{event_key}_final_p1", f"{event_key}_final_p2", event["final_score_max"])

    champion = "TBD"
    fp1 = st.session_state.get(f"{event_key}_final_p1")
    fp2 = st.session_state.get(f"{event_key}_final_p2")
    if fp1 is not None and fp2 is not None:
        if fp1 > fp2:
            champion = finalist_1
        elif fp2 > fp1:
            champion = finalist_2
    st.success(f"🏆 Champion: {champion}")


def render_super4(event_name, event):
    winners = render_group_stage(event_name, event)
    event_key = slug(event_name)
    st.subheader("Super 4 (Best of 3)")
    super4_players = [winners["A"], winners["B"]]
    runner_ups = []
    for group_name, players in event["groups"].items():
        standings = compute_group_standings(event_name, group_name, players)
        runner_ups.append(standings.iloc[1]["Player"] if len(standings) > 1 else f"{group_name}2")
    super4_players = [winners["A"], runner_ups[0], winners["B"], runner_ups[1]]

    labels = ["A1", "A2", "B1", "B2"]
    mapping_df = pd.DataFrame({"Slot": labels, "Player": super4_players})
    st.dataframe(mapping_df, use_container_width=True)

    for i in range(len(super4_players)):
        for j in range(i + 1, len(super4_players)):
            render_score_row(
                super4_players[i],
                super4_players[j],
                f"{event_key}_super4_{i}_{j}_p1",
                f"{event_key}_super4_{i}_{j}_p2",
                event["next_stage_score_max"],
            )

    standings = compute_knockout_round_robin(super4_players, f"{event_key}_super4")
    st.subheader("Super 4 Standings")
    st.dataframe(standings, use_container_width=True)
    st.info("Super 4 format: all matches are best of 3, each set played to 15 points.")


def render_super6(event_name, event):
    winners = render_group_stage(event_name, event)
    event_key = slug(event_name)
    st.subheader("Super 6 (Best of 3)")

    slots = []
    for group_name in ["A", "B", "C"]:
        players = event["groups"][group_name]
        standings = compute_group_standings(event_name, group_name, players)
        slot1 = standings.iloc[0]["Player"] if len(standings) > 0 else f"{group_name}1"
        slot2 = standings.iloc[1]["Player"] if len(standings) > 1 else f"{group_name}2"
        slots.extend([slot1, slot2])

    mapping_df = pd.DataFrame({
        "Slot": ["A1", "A2", "B1", "B2", "C1", "C2"],
        "Pair": slots,
    })
    st.dataframe(mapping_df, use_container_width=True)

    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            render_score_row(
                slots[i],
                slots[j],
                f"{event_key}_super6_{i}_{j}_p1",
                f"{event_key}_super6_{i}_{j}_p2",
                event["next_stage_score_max"],
            )

    standings = compute_knockout_round_robin(slots, f"{event_key}_super6")
    st.subheader("Super 6 Standings")
    st.dataframe(standings, use_container_width=True)

    finalist_1 = standings.iloc[0]["Player"] if len(standings) > 0 else "S6 - 1"
    finalist_2 = standings.iloc[1]["Player"] if len(standings) > 1 else "S6 - 2"
    st.subheader("Final (Best of 3)")
    render_score_row(finalist_1, finalist_2, f"{event_key}_final_p1", f"{event_key}_final_p2", event["final_score_max"])

    champion = "TBD"
    fp1 = st.session_state.get(f"{event_key}_final_p1")
    fp2 = st.session_state.get(f"{event_key}_final_p2")
    if fp1 is not None and fp2 is not None:
        if fp1 > fp2:
            champion = finalist_1
        elif fp2 > fp1:
            champion = finalist_2
    st.success(f"🏆 Champion: {champion}")
    st.info("Super 6 matches are best of 3 with each set to 15 points. Final is best of 3 with each set to 21 points.")


def render_groups_to_final(event_name, event):
    winners = render_group_stage(event_name, event)
    event_key = slug(event_name)
    st.subheader("Final (Best of 3)")

    group_names = list(event["groups"].keys())
    finalists = []
    if len(group_names) == 1:
        standings = compute_group_standings(event_name, group_names[0], event["groups"][group_names[0]])
        finalists = [
            standings.iloc[0]["Player"] if len(standings) > 0 else "A1",
            standings.iloc[1]["Player"] if len(standings) > 1 else "A2",
        ]
    else:
        finalists = [winners[group_names[0]], winners[group_names[1]]]

    render_score_row(finalists[0], finalists[1], f"{event_key}_final_p1", f"{event_key}_final_p2", event["final_score_max"])

    champion = "TBD"
    fp1 = st.session_state.get(f"{event_key}_final_p1")
    fp2 = st.session_state.get(f"{event_key}_final_p2")
    if fp1 is not None and fp2 is not None:
        if fp1 > fp2:
            champion = finalists[0]
        elif fp2 > fp1:
            champion = finalists[1]
    st.success(f"🏆 Champion: {champion}")
    st.info("Final match is best of 3 with each set played to 21 points.")


init_session_state()

st.title("🏓 TT Tournament Tracker")
st.caption(
    "Now includes Men's Singles, Men's Doubles, Women's Singles, Women's Doubles, and Mixed Doubles. "
    "Group stage is single set to 21. Knockout/super stages are best of 3 as per your format."
)

main_tabs = st.tabs(list(EVENTS.keys()))

for idx, (event_name, event) in enumerate(EVENTS.items()):
    with main_tabs[idx]:
        st.header(event_name)
        if event["type"] == "groups_to_round_robin_then_final":
            render_mens_singles(event_name, event)
        elif event["type"] == "groups_to_super6_then_final":
            render_super6(event_name, event)
        elif event["type"] == "groups_to_super4":
            render_super4(event_name, event)
        elif event["type"] == "groups_to_final":
            render_groups_to_final(event_name, event)

st.divider()
st.markdown("**Tiebreakers**")
st.write("Group stage: match wins → points difference → total points scored")
st.write("Super 4 / Super 6 / qualifier round robin: match wins → set difference → total sets won")
st.write("For best-of-3 stages, enter only valid results: 2-0, 2-1, 1-2, or 0-2.")
