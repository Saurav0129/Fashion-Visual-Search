# Import Libraries
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import streamlit as st
from PIL import Image
from db import ImageVectorDB
import base64
import io
import pandas as pd
import re
import json
import random
from datetime import datetime, timedelta

# Page Title
st.set_page_config(
    page_title="Fashion Visual Search",
    page_icon="👚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for UI
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .header {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        color: white;
        padding: 2rem;
        border-radius: 0 0 15px 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Product cards */
    .product-card {
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        padding: 15px;
        transition: all 0.3s ease;
        height: 100%;
        background: white;
        position: relative;
        overflow: hidden;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
    }
    
    .product-image-container {
        position: relative;
        overflow: hidden;
        border-radius: 10px;
        height: 300px;
        margin-bottom: 12px;
    }
    
    .product-image {
        object-fit: cover;
        width: 100%;
        height: 100%;
        transition: transform 0.5s ease;
    }
    
    .product-card:hover .product-image {
        transform: scale(1.05);
    }
    
    .product-badge {
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: #ff4757;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        z-index: 2;
    }
    
    .product-title {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 6px;
        height: 40px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        color: #2f3542;
    }
    
    .product-price {
        font-weight: 700;
        font-size: 18px;
        color: #ff6b81;
    }
    
    .product-mrp {
        text-decoration: line-through;
        color: #a4b0be;
        font-size: 14px;
        margin-left: 8px;
    }
    
    .product-discount {
        background-color: #2ed573;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }
    
    .similarity-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: rgba(255,255,255,0.9);
        color: #2f3542;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        z-index: 2;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .view-product-btn {
        background: linear-gradient(to right, #ff6b81, #ff4757) !important;
        color: white !important;
        border: none !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px rgba(255,107,129,0.3) !important;
        width: 100% !important;
    }
    
    .view-product-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(255,107,129,0.4) !important;
    }
    
    .disabled-btn {
        background: #a4b0be !important;
        color: white !important;
        border: none !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        cursor: not-allowed !important;
        width: 100% !important;
    }
    
    /* Similarity score */
    .similarity-score {
        font-size: 14px;
        font-weight: bold;
        color: #2f3542;
        margin-top: 8px;
    }
    
    .progress-bar {
        height: 6px;
        background: #dfe4ea;
        border-radius: 3px;
        margin-top: 5px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 3px;
    }
    
    /* Category selector */
    .category-selector {
        margin-bottom: 20px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px 0 0 15px;
    }
    
    /* Featured collections */
    .collection-card {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        margin-bottom: 15px;
    }
    
    .collection-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    
    .collection-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
        padding: 15px;
        color: white;
    }
    
    .collection-title {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 5px;
    }
    
    /* Upload area styling */
    .upload-area {
        border: 2px dashed #a4b0be;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        background: white;
        margin-bottom: 2rem;
    }
    
    .upload-area:hover {
        border-color: #ff6b81;
        background: rgba(255, 107, 129, 0.05);
    }
    
    .upload-instructions {
        margin-top: 1rem;
        font-size: 14px;
        color: #57606f;
    }
    
    /* Search results header */
    .results-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #dfe4ea;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    
    .badge-primary {
        background-color: #e3f2fd;
        color: #1976d2;
    }
    
    .badge-success {
        background-color: #e8f5e9;
        color: #388e3c;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
    
    /* File uploader customization */
    .stFileUploader > div > div {
        border: 2px dashed #a4b0be !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        background: white !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #ff6b81 !important;
        background: rgba(255, 107, 129, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1 style="color: white; margin: 0;">👗 Fashion Visual Search</h1>
    <p style="color: white; opacity: 0.9; margin: 0.5rem 0 0;">Upload an image to find similar fashion items from our collection</p>
</div>
""", unsafe_allow_html=True)

# Paths
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DRESSES_IMAGE_DIR = os.path.join(APP_DIR, "dresses_images")
DRESSES_METADATA_CSV = os.path.join(APP_DIR, "data", "dresses_with_image_paths.csv")
JEANS_IMAGE_DIR = os.path.join(APP_DIR, "jeans_images")
JEANS_METADATA_CSV = os.path.join(APP_DIR, "data", "jeans_with_image_paths.csv")

# DataBase Loading 
@st.cache_resource
def load_database(category):
    db = ImageVectorDB()
    with st.spinner(f"🔍 Loading {category} database..."):
        db.build_database_from_sources(
            image_folder=DRESSES_IMAGE_DIR if category == "Dresses" else JEANS_IMAGE_DIR,
            metadata_csv=DRESSES_METADATA_CSV if category == "Dresses" else JEANS_METADATA_CSV,
            st_ui=st,
            cache_dir="image_db_cache" 
        )
    return db

def clean_metadata_value(value):
    """Clean metadata values by removing brackets and unwanted characters"""
    if value is None or value == '' or str(value).lower() == 'nan':
        return 'N/A'
    
    # Convert to string
    value_str = str(value)
    
    value_str = re.sub(r'[\[\]{}]', '', value_str)
    
    # Remove quotes
    value_str = re.sub(r'["\']', '', value_str)
    
    # Clean up extra spaces
    value_str = re.sub(r'\s+', ' ', value_str).strip()
    
    try:
        if value_str.startswith('{') or value_str.startswith('['):
            parsed = json.loads(str(value))
            if isinstance(parsed, dict):
                # Extract meaningful values from dict
                meaningful_values = []
                for k, v in parsed.items():
                    if v and str(v).lower() not in ['nan', 'null', 'none', '']:
                        meaningful_values.append(f"{k}: {v}")
                return ', '.join(meaningful_values) if meaningful_values else 'N/A'
            elif isinstance(parsed, list):
                # Join list items
                return ', '.join([str(item) for item in parsed if item])
    except:
        pass
    
    return value_str if value_str and value_str != 'N/A' else 'N/A'

def safe_get_metadata(meta, possible_keys, default='N/A'):
    """Try multiple possible keys for a metadata field and clean the result"""
    if not isinstance(possible_keys, list):
        possible_keys = [possible_keys]
    
    for key in possible_keys:
        value = meta.get(key)
        cleaned_value = clean_metadata_value(value)
        if cleaned_value != 'N/A':
            return cleaned_value
    return default

def format_price(price_data):
    """Format price from dictionary or raw value"""
    if isinstance(price_data, dict):
        price = price_data.get('INR', 'N/A')
        try:
            return f"₹{float(price):,.2f}" if price != 'N/A' else 'N/A'
        except:
            return 'N/A'
    try:
        return f"₹{float(price_data):,.2f}" if price_data else 'N/A'
    except:
        return str(price_data) if price_data else 'N/A'

def format_discount(discount_data):
    """Format discount with 2 decimal places"""
    try:
        discount = float(discount_data)
        return f"{discount:.0f}% OFF"
    except:
        return "N/A"

def format_similarity(similarity_score):
    """Format similarity score with color coding"""
    similarity_percent = similarity_score * 100
    if similarity_percent >= 80:
        color = "#2ed573"  # Green
    elif similarity_percent >= 60:
        color = "#7bed9f"  # Light green
    elif similarity_percent >= 40:
        color = "#ffa502"  # Orange
    else:
        color = "#ff4757"  # Red
    
    progress_width = min(100, similarity_percent)
    
    return f"""
    <div class="similarity-badge">
        {similarity_percent:.0f}% Match
    </div>
    """

def is_recent_date(date_str, days=30):
    if date_str == 'N/A':
        return False
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - date_obj) < timedelta(days=days)
    except:
        return False

def get_smart_badge(meta):
    # Extract metadata
    discount = float(safe_get_metadata(meta, ['discount'], '0'))
    brand = safe_get_metadata(meta, ['brand'], '').lower()
    meta_info = safe_get_metadata(meta, ['meta_info'], '').lower()
    launch_date = safe_get_metadata(meta, ['launch_on'])
    last_seen = safe_get_metadata(meta, ['last_seen_date'])
    
    # Check for "Exclusive" (luxury brands or meta_info)
    if "gucci" in brand or "prada" in brand or "exclusive" in meta_info:
        return ("💎 Exclusive", "#ff6b81")
    
    # Check for "Sale" (high discount)
    elif discount > 30:
        return (f"🤑 {int(discount)}% OFF", "#ff6348")
    
    # Check for "New Arrival" (recent launch)
    elif is_recent_date(launch_date, days=30): 
        return ("🆕 New Arrival", "#2ed573")
    
    # Check for "Trending" (recently viewed)
    elif is_recent_date(last_seen, days=7):
        return ("🔥 Trending", "#ff4757")
    
    # Check for "Limited" (low stock)
    elif "limited" in meta_info or "low stock" in meta_info:
        return ("🚀 Limited", "#ffa502")
    
    # Default badge
    else:
        return ("⭐ Bestseller", "#3742fa")

def create_product_card(result, index):
    """Create a styled product card for display"""
    meta = result['metadata']
    pdp_url = safe_get_metadata(meta, ['pdp_url', 'pcip_url'], 'N/A')
    
    img_data = base64.b64decode(meta['image_data'])
    img = Image.open(io.BytesIO(img_data))
    
    # Get product information
    product_name = safe_get_metadata(meta, ['product_name', 'title'])
    brand = safe_get_metadata(meta, ['brand'])
    
    # Price information
    selling_price = format_price(meta.get('selling_price'))
    mrp = format_price(meta.get('mrp'))
    discount = format_discount(safe_get_metadata(meta, ['discount', 'discount_percentage', 'discount']))
    
    # Retrive badge
    badge_text, badge_color = get_smart_badge(meta) 
    
    # Create card
    card = f"""
    <div class="product-card fade-in" style="animation-delay: {index * 0.1}s;">
        <div class="product-image-container">
            <img src="data:image/png;base64,{meta['image_data']}" class="product-image">
            <div class="product-badge" style="background-color: {badge_color}">{badge_text}</div>
            {format_similarity(result['similarity'])}
        </div>
        <div class="product-title">{product_name}</div>
        <div style="color: #57606f; font-size: 14px; margin-bottom: 8px;">by {brand}</div>
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span class="product-price">{selling_price}</span>
            {f'<span class="product-mrp">{mrp}</span>' if mrp != 'N/A' and mrp != selling_price else ''}
            {f'<span class="product-discount">{discount}</span>' if discount != 'N/A' else ''}
        </div>
    </div>
    <div style="margin-top: 10px;">
        {f'<a href="{pdp_url}" target="_blank" style="text-decoration: none;"><button class="view-product-btn">🛍 View Product</button></a>' 
         if pdp_url != 'N/A' else 
         '<button class="disabled-btn" disabled>🔗 Link Not Available</button>'}
    </div>
    """
    return card

# SideBar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #2f3542;">🔍 Search Options</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Category selection
    category = st.radio(
        "Choose Category",
        ["Dresses", "Jeans"],
        index=0,
        key="category_select",
        format_func=lambda x: f"👗 {x}" if x == "Dresses" else f"👖 {x}"
    )
    
    st.markdown("---")
    
    st.markdown("**🔧 Search Parameters**")
    search_k = st.slider("Number of results", 3, 12, 6, help="How many similar items to show")
    similarity_threshold = st.slider("Similarity threshold", 0.0, 1.0, 0.5, 0.05, 
                                   help="Adjust how similar items must be to your query")
    
    st.markdown("---")
    st.markdown("**ℹ️ Database Info**")
    
    # Initialize database 
    try:
        db = load_database(category)
        st.success(f"**{category} database loaded successfully**")
        st.info(f"**Total Items:** {db.index.ntotal}")
    except Exception as e:
        st.error(f"Failed to load database: {str(e)}")
        st.stop()
    
    if st.button("🔄 Refresh Database", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    **✨ Features:**
    - Visual similarity search
    - Price comparison
    - Style matching
    - Instant product discovery
    
    **📱 Like a shopping app:**
    - Modern UI
    - Product badges
    - Smooth animations
    - Responsive design
    """)

# Search Area
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <h2 style="color: #2f3542;">📤 Upload Your Fashion Inspiration</h2>
    <p style="color: #57606f;">Drag & drop an image here or click to browse</p>
</div>
""", unsafe_allow_html=True)


query_file = st.file_uploader(
    "Fashion image upload",  
    type=["png", "jpg", "jpeg"],
    help="Upload an image of fashion item you like",
    label_visibility="hidden", 
    accept_multiple_files=False
)

if query_file:
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color: #2f3542; margin-bottom: 1rem;">Your Style Inspiration</h3>
        </div>
        """, unsafe_allow_html=True)
        
        query_image = Image.open(query_file).convert("RGB")
        st.image(query_image, use_container_width=True)
        
    with col2:
        st.markdown("""
        <div class="results-header">
            <h3 style="color: #2f3542; margin: 0;">Recommended For You</h3>
            <div>
                <span class="badge badge-primary">{search_k} items</span>
                <span class="badge badge-success">{category}</span>
            </div>
        </div>
        """.format(search_k=search_k, category=category), unsafe_allow_html=True)
        
        with st.spinner("✨ Finding your perfect fashion matches..."):
            results = db.search_similar_images(query_image, k=search_k, threshold=similarity_threshold)
        
        if not results:
            st.info("No similar items found. Try another image or adjust the similarity threshold.")
        else:
            if len(results) <= 3:
                cols = st.columns(len(results))
            else:
                cols = st.columns(3)
            
            for i, result in enumerate(results):
                with cols[i % 3]:
                    st.markdown(create_product_card(result, i), unsafe_allow_html=True)
                    with st.expander("📝 Product Details", expanded=False):
                        meta = result['metadata']
                        
                        # Get metadata
                        product_id = safe_get_metadata(meta, ['product_id'])
                        sku = safe_get_metadata(meta, ['sku'])
                        category = safe_get_metadata(meta, ['category_id', 'category'])
                        department = safe_get_metadata(meta, ['department_id', 'department'])
                        style_info = safe_get_metadata(meta, ['style_attributes', 'style'])
                        description = safe_get_metadata(meta, ['description'])
                        meta_info = safe_get_metadata(meta, ['meta_info'])
                        launch_date = safe_get_metadata(meta, ['launch_on', 'launch_date'])
                        last_seen = safe_get_metadata(meta, ['last_seen_date', 'last_seen'])
                        
                        # Display information 
                        st.markdown("""
                        <style>
                            .detail-row {
                                display: flex;
                                margin-bottom: 8px;
                            }
                            .detail-label {
                                font-weight: 600;
                                min-width: 120px;
                                color: #57606f;
                            }
                            .detail-value {
                                color: #2f3542;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        details = []
                        
                        if product_id != 'N/A':
                            details.append(("Product ID", product_id))
                        if sku != 'N/A':
                            details.append(("SKU", sku))
                        if category != 'N/A':
                            details.append(("Category", category))
                        if department != 'N/A':
                            details.append(("Department", department))
                        if style_info != 'N/A':
                            details.append(("Style", style_info))
                        if launch_date != 'N/A':
                            details.append(("Launch Date", launch_date))
                        if last_seen != 'N/A':
                            details.append(("Last Seen", last_seen))
                        
                        for label, value in details:
                            st.markdown(f"""
                            <div class="detail-row">
                                <div class="detail-label">{label}:</div>
                                <div class="detail-value">{value}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        if description != 'N/A':
                            st.markdown("---")
                            st.markdown("**Description**")
                            st.markdown(f"<div style='color: #2f3542;'>{description}</div>", unsafe_allow_html=True)
                        
                        if meta_info != 'N/A':
                            st.markdown("---")
                            st.markdown("**Additional Info**")
                            st.markdown(f"<div style='color: #2f3542;'>{meta_info}</div>", unsafe_allow_html=True)

# Featured Collections 
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h2 style="color: #2f3542;">🌟 Trending Collections</h2>
    <p style="color: #57606f;">Discover our most popular styles this season</p>
</div>
""", unsafe_allow_html=True)

# Featured collections with images and redirect URLs
featured_collections = [
    {
        "name": "Summer Dresses",
        "image": "https://media.karenmillen.com/i/karenmillen/bkk24436_chartreuse_xl?$product_image_category_page_horizontal_filters_desktop_2x$&fmt=webp",
        "url": "https://www.karenmillen.com/womens/edits/summer",
        "description": "Lightweight and breezy styles for sunny days"
    },
    {
        "name": "Occasion Dresses",
        "image": "https://media.karenmillen.com/i/karenmillen/bkk24328_blue_xl?$product_image_category_page_horizontal_filters_desktop_2x$&fmt=webp",
        "url": "https://www.karenmillen.com/womens/dresses/occasion-dresses",
        "description": "Elegant dresses for special events"
    },
    {
        "name": "Denim Wear",
        "image": "https://media.karenmillen.com/i/karenmillen/bkk24148_light%20blue_xl?$product_image_category_page_horizontal_filters_desktop_2x$&fmt=webp",
        "url": "https://www.karenmillen.com/womens/denim",
        "description": "Classic and contemporary denim styles"
    },
    {
        "name": "Work Dresses",
        "image": "https://media.karenmillen.com/i/karenmillen/bkk15686_ivory_xl?$product_image_category_page_horizontal_filters_desktop_2x$&fmt=webp",
        "url": "https://www.karenmillen.com/womens/work/dresses",
        "description": "Professional styles for the office"
    } 
]

# Display featured collections 
cols = st.columns(4)
for i, collection in enumerate(featured_collections):
    with cols[i]:
        st.markdown(f"""
        <div class="collection-card">
            <img src="{collection['image']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div class="collection-overlay">
                <div class="collection-title">{collection['name']}</div>
                <div style="font-size: 14px;">{collection['description']}</div>
            </div>
        </div>
        <a href="{collection['url']}" target="_blank" style="text-decoration: none;">
            <button class="view-product-btn" style="margin-top: 8px;">Explore Collection</button>
        </a>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #57606f; padding: 1.5rem 0;">
    <p>© 2025 Fashion Visual Search | Made with ❤️ for fashion lovers</p>
</div>
""", unsafe_allow_html=True)