# 👗 Fashion Visual Search  

**Find similar fashion items instantly using AI-powered visual search!**  

🔍 **Upload an image** → 🚀 **Get matching dresses/jeans** → 🛍️ **Shop the look**  

---

## 🌟 Preview  

| **Home Screen** | **Dress Search** | **Jeans Search** |
|----------------|----------------|----------------|
| ![App Preview](https://github.com/user-attachments/assets/2bf20073-ea21-469e-8542-3d4cc2aa4c0b) | ![Dress Search](https://github.com/user-attachments/assets/81a94288-4ec9-4030-9f49-ed8798c347ca) | ![Jeans Search](https://github.com/user-attachments/assets/b7020972-ed7a-46a5-83ab-9c40cdc3cfc6) |

---

## ✨ Features  

- **🖼️ Image-Based Search**  
  Upload a photo of a dress/jeans to find visually similar items.  
- **🎯 Smart Product Badges**  
  Auto-tagged badges like `Trending`, `New Arrival`, or `Exclusive` based on metadata.  
- **🔢 Dynamic Filtering**  
  Adjust similarity threshold and number of results.  
- **🛒 Direct Product Links**  
  Click "View Product" to visit the PDP (Product Display Page).  

---

## 📊 Data Schema  
Metadata includes:  
```python
{
  "product_id": "12345",
  "brand": "Zara",
  "product_name": "Floral Maxi Dress",
  "selling_price": "₹2,499",
  "mrp": "₹3,999",
  "discount": "38%",
  "pdp_url": "https://example.com/p/12345",
  "launch_on": "2025-05-20",  # Used for "New Arrival" badges
  "last_seen_date": "2025-06-10",  # Used for "Trending" badges
  "meta_info": "limited edition"  # Used for "Exclusive/Limited" badges
}
```

