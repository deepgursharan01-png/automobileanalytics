import base64
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------------------------------------------------
# 1. PAGE CONFIGURATION & GLOBAL STYLES
# -------------------------------------------------------------------
st.set_page_config(
    page_title="AutoMobile Analytics Portal",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Helper function to convert local image to base64 for CSS background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Try encoding background image (fallback gracefully if file isn't found)
try:
    img_base64 = get_base64_of_bin_file("por.webp")
    bg_style = f"""
        background: linear-gradient(rgba(10, 15, 30, 0.75), rgba(10, 15, 30, 0.85)), 
                    url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
    """
except Exception:
    bg_style = "background: linear-gradient(135deg, #0f172a 0%, #095ebe 100%);"

# Inject Custom CSS
st.markdown(
    f"""
<style>
    .stApp {{
        {bg_style}
        color: #f8fafc;
    }}
    
    /* Enhanced Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    
    .sidebar-header {{
        text-align: center;
        padding: 15px 10px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        margin-bottom: 20px;
        backdrop-filter: blur(8px);
    }}

    .sidebar-header h2 {{
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #38bdf8 !important;
        margin: 0 !important;
        letter-spacing: 0.5px;
    }}

    .sidebar-header p {{
        font-size: 0.75rem !important;
        color: #94a3b8 !important;
        margin: 4px 0 0 0 !important;
    }}

    /* Custom Attractive Navigation Box Options */
    .stButton > button {{
        width: 100%;
        background: rgba(30, 41, 59, 0.6) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-align: left !important;
        transition: all 0.25s ease-in-out !important;
        margin-bottom: 2px !important;
        backdrop-filter: blur(4px);
    }}

    .stButton > button:hover {{
        background: rgba(56, 189, 248, 0.2) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);
    }}

    /* Selected Navigation Item Box Styling */
    .nav-active > button {{
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4) !important;
        font-weight: 700 !important;
    }}
    
    .hero-banner {{
        background: rgba(15, 23, 42, 0.65);
        color: #095ebe;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }}
    
    .feature-card {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .feature-card:hover {{
        border-color: #38bdf8;
        transform: translateY(-2px);
    }}
    
    .metric-badge {{
        background: rgba(56, 189, 248, 0.2);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }}

    .tag-chip {{
        background: rgba(30, 41, 59, 0.8);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-right: 6px;
    }}
</style>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# 2. DATA LOADING & VALIDATION
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("SalesCars.csv")
    required_cols = [
        "Price_INR",
        "Units_Sold",
        "Brand",
        "Model",
        "Top_Speed",
        "Mileage_kmpl",
        "Fuel_Type",
        "Body_Type",
        "Transmission",
        "Horsepower",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns in CSV: {', '.join(missing)}"
        )

    df["Total_Revenue_INR"] = df["Price_INR"] * df["Units_Sold"]
    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"🚨 Error loading dataset: {e}")
    st.stop()


# -------------------------------------------------------------------
# PAGE 1: INTRODUCTION & HIGHLIGHTS
# -------------------------------------------------------------------
def page_intro():
    st.markdown(
        """
    <div class="hero-banner">
        <span class="metric-badge"> Introduction</span>
        <h1 style="margin-top: 10px; font-size: 2.8rem; font-weight: 700; color: #ffffff;">
            Automobile Analytics Portal 🏎️ 
        </h1>
        <p style="font-size: 1.1rem; color: #cbd5e1; max-width: 850px; margin-bottom: 0px;">
            An interactive executive analytics portal analyzing vehicle inventory, engine performance, pricing trends, 
            and market demand across top automotive brands.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("📌 Total Dataset Summary")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Cars Cataloged", f"{len(df):,}")
    s2.metric("Unique Brands", f"{df['Brand'].nunique()}")
    s3.metric(
        "Gross Revenue", f"₹{df['Total_Revenue_INR'].sum()/1e7:,.1f} Cr"
    )
    s4.metric("Total Vehicles Sold", f"{df['Units_Sold'].sum():,}")

    st.markdown("---")
    st.subheader("🌟 Executive Snapshot & Record Highlights")

    top_seller = df.loc[df["Units_Sold"].idxmax()]
    fastest_car = df.loc[df["Top_Speed"].idxmax()]
    most_efficient = df.loc[df["Mileage_kmpl"].idxmax()]
    most_expensive = df.loc[df["Price_INR"].idxmax()]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
        <div class="feature-card">
            <span class="metric-badge">🔥 Best Seller</span>
            <h4 style="margin: 5px 0; color: #f8fafc;">{top_seller['Brand']} {top_seller['Model']}</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">Units Sold: <b>{top_seller['Units_Sold']:,}</b></p>
            <span class="tag-chip">{top_seller['Fuel_Type']}</span>
            <span class="tag-chip">{top_seller['Body_Type']}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
        <div class="feature-card">
            <span class="metric-badge">⚡ Highest Speed</span>
            <h4 style="margin: 5px 0; color: #f8fafc;">{fastest_car['Brand']} {fastest_car['Model']}</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">Top Speed: <b>{fastest_car['Top_Speed']} km/h</b></p>
            <span class="tag-chip">{fastest_car['Horsepower']} HP</span>
            <span class="tag-chip">{fastest_car['Transmission']}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
        <div class="feature-card">
            <span class="metric-badge">🌱 Fuel Eco Leader</span>
            <h4 style="margin: 5px 0; color: #f8fafc;">{most_efficient['Brand']} {most_efficient['Model']}</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">Mileage: <b>{most_efficient['Mileage_kmpl']} km/l</b></p>
            <span class="tag-chip">{most_efficient['Fuel_Type']}</span>
            <span class="tag-chip">{most_efficient['Body_Type']}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
        <div class="feature-card">
            <span class="metric-badge">💎 Flagship Luxury</span>
            <h4 style="margin: 5px 0; color: #f8fafc;">{most_expensive['Brand']} {most_expensive['Model']}</h4>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">Price: <b>₹{most_expensive['Price_INR']/1e7:.2f} Cr</b></p>
            <span class="tag-chip">{most_expensive['Transmission']}</span>
            <span class="tag-chip">{most_expensive['Fuel_Type']}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

# -------------------------------------------------------------------
# PAGE 2: SEARCH RECORDS
# -------------------------------------------------------------------
def page_search():
    st.title("🔍 Search & Find Car Records")
    st.caption(
        "Filter through vehicle records based on specifications and pricing."
    )
    st.markdown("---")

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        selected_brand = st.multiselect("Brand", sorted(df["Brand"].unique()))
    with f2:
        selected_fuel = st.multiselect(
            "Fuel Type", sorted(df["Fuel_Type"].unique())
        )
    with f3:
        selected_body = st.multiselect(
            "Body / Car Type", sorted(df["Body_Type"].unique())
        )
    with f4:
        selected_trans = st.multiselect(
            "Transmission", sorted(df["Transmission"].unique())
        )

    p1, p2, p3 = st.columns(3)
    with p1:
        min_price, max_price = int(df["Price_INR"].min()), int(
            df["Price_INR"].max()
        )
        price_range = st.slider(
            "Price Range (INR)",
            min_price,
            max_price,
            (min_price, max_price),
            step=100000,
        )
    with p2:
        min_hp, max_hp = int(df["Horsepower"].min()), int(
            df["Horsepower"].max()
        )
        hp_range = st.slider(
            "Horsepower Range", min_hp, max_hp, (min_hp, max_hp), step=10
        )
    with p3:
        min_top, max_top = int(df["Top_Speed"].min()), int(
            df["Top_Speed"].max()
        )
        top_range = st.slider(
            "Top Speed (km/h)", min_top, max_top, (min_top, max_top), step=5
        )

    filtered = df.copy()
    if selected_brand:
        filtered = filtered[filtered["Brand"].isin(selected_brand)]
    if selected_fuel:
        filtered = filtered[filtered["Fuel_Type"].isin(selected_fuel)]
    if selected_body:
        filtered = filtered[filtered["Body_Type"].isin(selected_body)]
    if selected_trans:
        filtered = filtered[filtered["Transmission"].isin(selected_trans)]

    filtered = filtered[
        (filtered["Price_INR"].between(price_range[0], price_range[1]))
        & (filtered["Horsepower"].between(hp_range[0], hp_range[1]))
        & (filtered["Top_Speed"].between(top_range[0], top_range[1]))
    ]

    st.markdown("---")
    header_col, export_col = st.columns([3, 1])
    with header_col:
        st.subheader(f"Matching Records ({len(filtered):,} found)")
    with export_col:
        csv_data = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export CSV",
            data=csv_data,
            file_name="filtered_cars.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.dataframe(
        filtered[[
            "Brand",
            "Model",
            "Body_Type",
            "Transmission",
            "Fuel_Type",
            "Price_INR",
            "Horsepower",
            "Top_Speed",
            "Mileage_kmpl",
            "Units_Sold",
            "Total_Revenue_INR",
        ]],
        use_container_width=True,
        height=500,
    )


# -------------------------------------------------------------------
# PAGE 3: VISUAL DASHBOARD
# -------------------------------------------------------------------
def page_graphs():
    st.title("📊 Visual Analytics & Performance Dashboard")
    st.caption(
        "Customize dashboard filters in the sidebar to inspect sales and specifications charts."
    )
    st.markdown("---")

    st.sidebar.markdown("### 🎛️ Chart Filters")

    all_body_types = sorted(df["Body_Type"].unique())
    selected_body = st.sidebar.multiselect(
        "🚗 Car Type", all_body_types, default=all_body_types, key="g_body"
    )

    all_transmissions = sorted(df["Transmission"].unique())
    selected_trans = st.sidebar.multiselect(
        "⚙️ Transmission",
        all_transmissions,
        default=all_transmissions,
        key="g_trans",
    )

    all_fuels = sorted(df["Fuel_Type"].unique())
    selected_fuels = st.sidebar.multiselect(
        "⛽ Fuel Type", all_fuels, default=all_fuels, key="g_fuel"
    )

    all_brands = sorted(df["Brand"].unique())
    selected_brands = st.sidebar.multiselect(
        "🏷️ Brand", all_brands, default=all_brands, key="g_brand"
    )

    min_p, max_p = int(df["Price_INR"].min()), int(df["Price_INR"].max())
    selected_price = st.sidebar.slider(
        "💰 Price Range (INR)",
        min_p,
        max_p,
        (min_p, max_p),
        step=200000,
        key="g_price",
    )

    dash_df = df[
        (df["Body_Type"].isin(selected_body))
        & (df["Transmission"].isin(selected_trans))
        & (df["Fuel_Type"].isin(selected_fuels))
        & (df["Brand"].isin(selected_brands))
        & (df["Price_INR"].between(selected_price[0], selected_price[1]))
    ]

    if dash_df.empty:
        st.warning(
            "⚠️ No records match your current filter selections. Please broaden your sidebar filters."
        )
        st.stop()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        "Filtered Revenue", f"₹{dash_df['Total_Revenue_INR'].sum()/1e7:,.2f} Cr"
    )
    k2.metric("Filtered Units Sold", f"{dash_df['Units_Sold'].sum():,}")
    k3.metric("Avg Price", f"₹{dash_df['Price_INR'].mean():,.0f}")
    k4.metric("Avg Efficiency", f"{dash_df['Mileage_kmpl'].mean():.1f} km/l")

    st.markdown("---")

    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.subheader("📊 Revenue by Brand & Fuel Type")
        brand_fuel = (
            dash_df.groupby(["Brand", "Fuel_Type"])["Total_Revenue_INR"]
            .sum()
            .reset_index()
        )
        fig_brand = px.bar(
            brand_fuel,
            x="Brand",
            y="Total_Revenue_INR",
            color="Fuel_Type",
            barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={"Total_Revenue_INR": "Revenue (INR)", "Brand": "Brand"},
        )
        fig_brand.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_brand, use_container_width=True)

    with c2:
        st.subheader("⚙️ Transmission & Car Type Share")
        trans_body = (
            dash_df.groupby(["Body_Type", "Transmission"])["Units_Sold"]
            .sum()
            .reset_index()
        )
        fig_donut = px.sunburst(
            trans_body,
            path=["Body_Type", "Transmission"],
            values="Units_Sold",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_donut.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("⚡ Performance Matrix (HP vs. Mileage)")
        fig_scatter = px.scatter(
            dash_df,
            x="Horsepower",
            y="Mileage_kmpl",
            color="Body_Type",
            size="Units_Sold",
            hover_data=["Brand", "Model", "Price_INR", "Transmission"],
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_scatter.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c4:
        st.subheader("💰 Price Distribution by Car Type")
        fig_box = px.box(
            dash_df,
            x="Body_Type",
            y="Price_INR",
            color="Transmission",
            points="outliers",
            color_discrete_sequence=["#22f337", "#fd2626"],
        )
        fig_box.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("🏆 Top 10 Best Selling Vehicle Models")
    top_models = (
        dash_df.groupby(["Brand", "Model", "Body_Type"])["Units_Sold"]
        .sum()
        .reset_index()
    )
    top_models = top_models.sort_values(by="Units_Sold", ascending=False).head(
        10
    )

    fig_top = px.bar(
        top_models,
        x="Units_Sold",
        y="Model",
        color="Brand",
        orientation="h",
        text="Units_Sold",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_top.update_layout(
        template="plotly_dark",
        height=350,
        yaxis={"categoryorder": "total ascending"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_top, use_container_width=True)


# -------------------------------------------------------------------
# PAGE 4: SIMPLE INDIA MAP WITH CAR SEARCH FILTER
# -------------------------------------------------------------------
def page_map():
    st.title("🗺️ India Vehicle Map")

    # Major Indian Cities for Mapping Records
    locations = [
        {"City": "Mumbai", "State": "Maharashtra", "lat": 19.0760, "lon": 72.8777},
        {"City": "Delhi NCR", "State": "Delhi", "lat": 28.6139, "lon": 77.2090},
        {"City": "Bengaluru", "State": "Karnataka", "lat": 12.9716, "lon": 77.5946},
        {"City": "Chennai", "State": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707},
        {"City": "Ahmedabad", "State": "Gujarat", "lat": 23.0225, "lon": 72.5714},
        {"City": "Hyderabad", "State": "Telangana", "lat": 17.3850, "lon": 78.4867},
        {"City": "Kolkata", "State": "West Bengal", "lat": 22.5726, "lon": 88.3639},
        {"City": "Chandigarh", "State": "Punjab", "lat": 30.7333, "lon": 76.7794},
        {"City": "Lucknow", "State": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462},
        {"City": "Kochi", "State": "Kerala", "lat": 9.9312, "lon": 76.2673},
    ]

    # Map each CSV record to an Indian city location with slight jitter for visibility
    map_df = df.copy()
    loc_indices = np.arange(len(map_df)) % len(locations)

    map_df["City"] = [locations[i]["City"] for i in loc_indices]
    map_df["State"] = [locations[i]["State"] for i in loc_indices]
    map_df["lat"] = [
        locations[i]["lat"] + np.sin(idx) * 0.25 for idx, i in enumerate(loc_indices)
    ]
    map_df["lon"] = [
        locations[i]["lon"] + np.cos(idx) * 0.25 for idx, i in enumerate(loc_indices)
    ]

    # Combined label for searching
    map_df["Car_Display"] = map_df["Brand"] + " " + map_df["Model"]

    # --- CAR SEARCH FILTER ---
    car_list = ["All Cars"] + sorted(map_df["Car_Display"].unique().tolist())
    selected_car = st.selectbox(
        "🔍 Search & Highlight Particular Car on Map:",
        car_list,
        index=0,
        help="Type or select a car model to highlight its location on the map.",
    )

    # Filter dataset if a specific car is searched
    if selected_car != "All Cars":
        plot_df = map_df[map_df["Car_Display"] == selected_car]
        # Auto-center map on selected car location with higher zoom
        zoom_level = 6.0
        center_coords = {
            "lat": float(plot_df["lat"].iloc[0]),
            "lon": float(plot_df["lon"].iloc[0]),
        }

        # Display brief specs callout for searched car
        selected_row = plot_df.iloc[0]
        st.info(
            f"📍 **Location:** {selected_row['City']}, {selected_row['State']} | "
            f"💰 **Price:** ₹{selected_row['Price_INR']:,.0f} | "
            f"⛽ **Fuel:** {selected_row['Fuel_Type']} | "
            f"⚡ **Top Speed:** {selected_row['Top_Speed']} km/h | "
            f"🌱 **Mileage:** {selected_row['Mileage_kmpl']} km/l"
        )
    else:
        plot_df = map_df
        zoom_level = 3.8
        center_coords = {"lat": 22.5937, "lon": 78.9629}

    # Render India Map with filtered/highlighted records
    fig_map = px.scatter_mapbox(
        plot_df,
        lat="lat",
        lon="lon",
        color="Brand",
        size="Units_Sold",
        hover_name="Model",
        hover_data={
            "Brand": True,
            "City": True,
            "State": True,
            "Price_INR": ":,.0f",
            "Units_Sold": ":,",
            "Fuel_Type": True,
            "Transmission": True,
            "lat": False,
            "lon": False,
        },
        zoom=zoom_level,
        center=center_coords,
        mapbox_style="carto-darkmatter",
    )

    fig_map.update_layout(
        template="plotly_dark",
        height=620,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig_map, use_container_width=True)


# -------------------------------------------------------------------
# ROUTER & ENHANCED SIDEBAR NAVIGATION
# -------------------------------------------------------------------
if "page_select" not in st.session_state:
    st.session_state["page_select"] = "Introduction"

# Custom Header inside Sidebar
st.sidebar.markdown(
    """
    <div class="sidebar-header">
        <h2>🏎️ Auto Analytics</h2>
        <p>Control Center & Navigation</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Navigation Options Definition
nav_options = [
    {"label": "🏠  Introduction", "value": "Introduction"},
    {"label": "🔍  Search Records", "value": "Search Records"},
    {"label": "📊  Visual Dashboard", "value": "Visual Dashboard"},
    {"label": "🗺️  India Map", "value": "Map"},
]

# Render Custom Box Navigation Buttons
for opt in nav_options:
    is_active = st.session_state["page_select"] == opt["value"]
    
    # Wrap in active container if currently selected for custom CSS accenting
    if is_active:
        st.sidebar.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.sidebar.button(opt["label"], key=f"btn_{opt['value']}", use_container_width=True):
            pass
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    else:
        if st.sidebar.button(opt["label"], key=f"btn_{opt['value']}", use_container_width=True):
            st.session_state["page_select"] = opt["value"]
            st.rerun()

st.sidebar.markdown("---")

# Route Page Execution
page_choice = st.session_state["page_select"]

if page_choice == "Introduction":
    page_intro()
elif page_choice == "Search Records":
    page_search()
elif page_choice == "Visual Dashboard":
    page_graphs()
elif page_choice == "Map":
    page_map()