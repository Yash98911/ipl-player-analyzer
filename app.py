
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('ipl_cleaned.csv')

team_short = {
    'Royal Challengers Bangalore': 'RCB',
    'Mumbai Indians': 'MI',
    'Chennai Super Kings': 'CSK',
    'Kolkata Knight Riders': 'KKR',
    'Delhi Capitals': 'DC',
    'Punjab Kings': 'PBKS',
    'Rajasthan Royals': 'RR',
    'Sunrisers Hyderabad': 'SRH',
    'Deccan Chargers': 'DC Old',
    'Gujarat Titans': 'GT',
    'Lucknow Super Giants': 'LSG',
    'Rising Pune Supergiants': 'RPS',
    'Gujarat Lions': 'GL',
    'Kochi Tuskers Kerala': 'KTK',
    'Pune Warriors': 'PW'
}

batters = sorted(
    df.groupby('batter')
    .filter(lambda x: len(x) >= 50)['batter']
    .unique().tolist()
)
bowlers = sorted(
    df.groupby('bowler')
    .filter(lambda x: len(x) >= 50)['bowler']
    .unique().tolist()
)

st.set_page_config(page_title="IPL Player Analyzer",
                   page_icon="🏏", layout="wide")

st.title("🏏 IPL Player Analyzer")
st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["📊 Player Analyzer", 
                       "⚔️ Head to Head"])

# ─── TAB 1 — PLAYER ANALYZER ──────────────────────
with tab1:

    player_type = st.radio("Select Player Type",
                            ['🏏 Batter', '🎯 Bowler'],
                            horizontal=True)

    # ── BATTER ──
    if player_type == '🏏 Batter':

        player = st.selectbox("Select Batter", batters)

        if st.button("Analyze 🔍",
                     use_container_width=True,
                     key='batter_btn'):

            player_df = df[df['batter'] == player]

            # Stats
            total_runs    = player_df['batsman_runs'].sum()
            total_matches = player_df['match_id'].nunique()
            career_avg    = round(
                player_df.groupby('match_id')['batsman_runs']
                         .sum().mean(), 2)
            career_sr     = round(
                total_runs / len(player_df) * 100, 2)
            highest_score = player_df.groupby('match_id')\
                                      ['batsman_runs']\
                                      .sum().max()

            st.markdown("---")
            st.subheader(f"📊 {player} — Career Stats")

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("🏏 Total Runs",     f"{total_runs:,}")
            col2.metric("📅 Matches Played", f"{total_matches}")
            col3.metric("📈 Career Average", f"{career_avg}")
            col4.metric("⚡ Strike Rate",    f"{career_sr}")
            col5.metric("🌟 Highest Score",  f"{highest_score}")

            st.markdown("---")

            # Season wise performance
            st.subheader("📅 Season Wise Performance")

            season_runs = df[df['batter'] == player]\
                           .merge(
                               df[['match_id','season']]\
                               .drop_duplicates(),
                               on='match_id'
                           )\
                           .groupby('season_y')['batsman_runs']\
                           .sum().reset_index()
            season_runs.columns = ['Season', 'Runs']

            fig0, ax0 = plt.subplots(figsize=(10, 4))
            bars0 = ax0.bar(season_runs['Season'],
                            season_runs['Runs'],
                            color='#2196F3',
                            edgecolor='white')
            for bar in bars0:
                ax0.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 10,
                         f'{int(bar.get_height())}',
                         ha='center', fontsize=9)
            ax0.set_xlabel('Season')
            ax0.set_ylabel('Total Runs')
            ax0.set_title(f'{player} — Runs Per Season')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig0)

            st.markdown("---")

            # Top 3 Venues
            st.subheader("🏟️ Top 3 Performing Venues")

            top_venues = player_df.groupby('venue')\
                                   ['batsman_runs']\
                                   .mean()\
                                   .sort_values(ascending=False)\
                                   .head(3).reset_index()
            top_venues.columns = ['Venue', 'Avg Runs']
            top_venues['Avg Runs'] = top_venues['Avg Runs'].round(2)
            top_venues['Venue'] = top_venues['Venue']\
                                   .apply(lambda x: x[:25] + '...'
                                          if len(x) > 25 else x)

            fig1, ax1 = plt.subplots(figsize=(8, 4))
            bars = ax1.barh(top_venues['Venue'],
                            top_venues['Avg Runs'],
                            color=['#2196F3','#4CAF50','#FF9800'])
            for bar, val in zip(bars, top_venues['Avg Runs']):
                ax1.text(bar.get_width() + 0.3,
                         bar.get_y() + bar.get_height()/2,
                         f'{val}', va='center', fontsize=11)
            ax1.set_xlabel('Average Runs')
            ax1.set_title(f'{player} — Best Venues')
            plt.tight_layout()
            st.pyplot(fig1)

            st.markdown("---")

            # SR vs Teams
            st.subheader("⚔️ Strike Rate vs Each Team")

            sr_vs_teams = player_df.groupby('bowling_team')\
                                    .apply(lambda x: round(
                                        x['batsman_runs'].sum() /
                                        len(x) * 100, 2))\
                                    .sort_values(ascending=False)\
                                    .reset_index()
            sr_vs_teams.columns = ['Team', 'Strike Rate']
            sr_vs_teams['Team'] = sr_vs_teams['Team']\
                                   .map(team_short)\
                                   .fillna(sr_vs_teams['Team'])

            fig2, ax2 = plt.subplots(figsize=(10, 5))
            bars2 = ax2.bar(sr_vs_teams['Team'],
                            sr_vs_teams['Strike Rate'],
                            color='#2196F3', edgecolor='white')
            for bar in bars2:
                ax2.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 0.5,
                         f'{bar.get_height():.1f}',
                         ha='center', fontsize=9)
            ax2.set_xlabel('Team')
            ax2.set_ylabel('Strike Rate')
            ax2.set_title(f'{player} — Strike Rate vs Teams')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig2)

    # ── BOWLER ──
    else:

        player = st.selectbox("Select Bowler", bowlers)

        if st.button("Analyze 🔍",
                     use_container_width=True,
                     key='bowler_btn'):

            player_df = df[df['bowler'] == player]

            # Stats
            total_wickets  = int(player_df['is_wicket'].sum())
            total_matches  = player_df['match_id'].nunique()
            career_economy = round(
                player_df['total_runs'].sum() /
                len(player_df) * 6, 2)
            avg_wickets    = round(
                player_df.groupby('match_id')['is_wicket']
                         .sum().mean(), 2)
            best_match     = int(
                player_df.groupby('match_id')['is_wicket']
                         .sum().max())

            st.markdown("---")
            st.subheader(f"📊 {player} — Career Stats")

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("🎯 Total Wickets",     f"{total_wickets}")
            col2.metric("📅 Matches Played",    f"{total_matches}")
            col3.metric("💰 Career Economy",    f"{career_economy}")
            col4.metric("📊 Avg Wickets/Match", f"{avg_wickets}")
            col5.metric("🌟 Best Match",        f"{best_match} wkts")

            st.markdown("---")

            # Season wise wickets
            st.subheader("📅 Season Wise Wickets")

            season_wkts = df[df['bowler'] == player]\
                           .merge(
                               df[['match_id','season']]\
                               .drop_duplicates(),
                               on='match_id'
                           )\
                           .groupby('season_y')['is_wicket']\
                           .sum().reset_index()
            season_wkts.columns = ['Season', 'Wickets']

            fig0, ax0 = plt.subplots(figsize=(10, 4))
            bars0 = ax0.bar(season_wkts['Season'],
                            season_wkts['Wickets'],
                            color='#9C27B0',
                            edgecolor='white')
            for bar in bars0:
                ax0.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 0.2,
                         f'{int(bar.get_height())}',
                         ha='center', fontsize=9)
            ax0.set_xlabel('Season')
            ax0.set_ylabel('Total Wickets')
            ax0.set_title(f'{player} — Wickets Per Season')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig0)

            st.markdown("---")

            # Top 3 Venues
            st.subheader("🏟️ Top 3 Venues — Most Wickets")

            top_venues = player_df.groupby('venue')\
                                   ['is_wicket']\
                                   .sum()\
                                   .sort_values(ascending=False)\
                                   .head(3).reset_index()
            top_venues.columns = ['Venue', 'Wickets']
            top_venues['Venue'] = top_venues['Venue']\
                                   .apply(lambda x: x[:25] + '...'
                                          if len(x) > 25 else x)

            fig1, ax1 = plt.subplots(figsize=(8, 4))
            bars = ax1.barh(top_venues['Venue'],
                            top_venues['Wickets'],
                            color=['#E91E63','#9C27B0','#FF5722'])
            for bar, val in zip(bars, top_venues['Wickets']):
                ax1.text(bar.get_width() + 0.1,
                         bar.get_y() + bar.get_height()/2,
                         f'{int(val)}', va='center', fontsize=11)
            ax1.set_xlabel('Total Wickets')
            ax1.set_title(f'{player} — Best Venues')
            plt.tight_layout()
            st.pyplot(fig1)

            st.markdown("---")

            # Wickets vs Teams
            st.subheader("⚔️ Wickets vs Each Team")

            wickets_vs_teams = player_df.groupby('batting_team')\
                                         ['is_wicket']\
                                         .sum()\
                                         .sort_values(ascending=False)\
                                         .reset_index()
            wickets_vs_teams.columns = ['Team', 'Wickets']
            wickets_vs_teams['Team'] = wickets_vs_teams['Team']\
                                        .map(team_short)\
                                        .fillna(wickets_vs_teams['Team'])

            fig2, ax2 = plt.subplots(figsize=(10, 5))
            bars2 = ax2.bar(wickets_vs_teams['Team'],
                            wickets_vs_teams['Wickets'],
                            color='#9C27B0', edgecolor='white')
            for bar in bars2:
                ax2.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 0.1,
                         f'{int(bar.get_height())}',
                         ha='center', fontsize=9)
            ax2.set_xlabel('Team')
            ax2.set_ylabel('Wickets')
            ax2.set_title(f'{player} — Wickets vs Teams')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig2)

# ─── TAB 2 — HEAD TO HEAD ─────────────────────────
with tab2:

    st.subheader("⚔️ Batter vs Bowler — Head to Head")
    st.write("Who dominates? Find out with data!")

    col1, col2 = st.columns(2)

    with col1:
        h2h_batter = st.selectbox("Select Batter",
                                   batters,
                                   key='h2h_batter')
    with col2:
        h2h_bowler = st.selectbox("Select Bowler",
                                   bowlers,
                                   key='h2h_bowler')

    if st.button("Compare ⚔️", use_container_width=True):

        # Filter
        h2h_df = df[(df['batter'] == h2h_batter) &
                    (df['bowler'] == h2h_bowler)]

        if len(h2h_df) == 0:
            st.warning("These two players never faced "
                       "each other!")
        else:
            balls_faced  = len(h2h_df)
            runs_scored  = h2h_df['batsman_runs'].sum()
            times_out    = h2h_df['is_wicket'].sum()
            strike_rate  = round(runs_scored / balls_faced * 100, 2)
            dot_balls    = len(h2h_df[h2h_df['batsman_runs'] == 0])
            dot_pct      = round(dot_balls / balls_faced * 100, 1)
            fours        = len(h2h_df[h2h_df['batsman_runs'] == 4])
            sixes        = len(h2h_df[h2h_df['batsman_runs'] == 6])

            # Verdict
            if strike_rate > 130 and times_out <= 2:
                verdict       = "🟢 Batter Dominates"
                verdict_color = "green"
            elif strike_rate < 100 and times_out >= 3:
                verdict       = "🔴 Bowler Dominates"
                verdict_color = "red"
            else:
                verdict       = "🟡 Competitive Battle"
                verdict_color = "orange"

            st.markdown("---")
            st.subheader(f"{h2h_batter} vs {h2h_bowler}")
            st.markdown(f"### Verdict: {verdict}")

            st.markdown("---")

            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("🏏 Runs Scored",  f"{runs_scored}")
            col2.metric("🎯 Times Out",    f"{times_out}")
            col3.metric("⚡ Strike Rate",  f"{strike_rate}")

            col4, col5, col6 = st.columns(3)
            col4.metric("🎳 Balls Faced",  f"{balls_faced}")
            col5.metric("⚫ Dot Ball %",   f"{dot_pct}%")
            col6.metric("💥 4s / 6s",     f"{fours} / {sixes}")

            st.markdown("---")

            # Runs breakdown chart
            st.subheader("📊 Runs Breakdown")

            runs_count = h2h_df['batsman_runs']\
                                .value_counts()\
                                .sort_index()

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(runs_count.index.astype(str),
                   runs_count.values,
                   color='#2196F3', edgecolor='white')
            ax.set_xlabel('Runs Per Ball')
            ax.set_ylabel('Count')
            ax.set_title(f'{h2h_batter} vs {h2h_bowler} '
                         f'— Ball by Ball Breakdown')
            for i, v in enumerate(runs_count.values):
                ax.text(i, v + 0.3, str(v),
                        ha='center', fontsize=10)
            plt.tight_layout()
            st.pyplot(fig)