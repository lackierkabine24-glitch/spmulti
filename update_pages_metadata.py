#!/usr/bin/env python3
"""
Update all Astro pages with H1 headings and meta descriptions.
"""
import os
import re
from pathlib import Path

# Page metadata mapping with H1 and meta descriptions
page_metadata = {
    'index.astro': {  # Home page
        'h1': 'Salespeare – Industrial Machinery & Powder Coating Equipment Supplier Since 2010',
        'description': 'Leading supplier of CNC machines, powder coating equipment, and industrial machinery for UAE, GCC, and worldwide. 15+ years experience in automation, installation, and support.'
    },
    'about-us/index.astro': {
        'h1': 'About Salespeare – Engineering Excellence Since 2010',
        'description': 'Learn about Salespeare\'s 15+ years of experience in powder coating lines, CNC machinery, and industrial solutions. Global partner for equipment supply, installation, and support.'
    },
    'contact/index.astro': {
        'h1': 'Contact Salespeare – Get in Touch With Our Engineering Team',
        'description': 'Contact Salespeare for CNC machines, powder coating equipment, pricing, availability, installation support, and technical advice. Fast response, global shipping available.'
    },
    'powdercoat-equipment/index.astro': {
        'h1': 'Powder Coating Equipment for Sale – Manual & Automated Coating Plants',
        'description': 'Powder coating equipment supplier offering manual and automated coating plants, spray guns, ovens, booths, and complete turnkey systems worldwide.'
    },
    'polished-marble/index.astro': {
        'h1': 'Polished Marble – High-Quality Finishing & Processing',
        'description': 'Explore polished marble products and processing equipment. Specialized machinery for marble finishing, cutting, and production in UAE and GCC.'
    },
    'cnc-machine-supplier/index.astro': {
        'h1': 'CNC Machines for Sale – Fiber Laser, Milling, Lathes & More',
        'description': 'CNC machines supplier in UAE offering fiber laser cutting, CNC milling, lathes, woodworking equipment, used machines, with delivery and support across GCC.'
    },
    'dubai-rak-flat-finder/index.astro': {
        'h1': 'Dubai & RAK Flat Finder – Real Estate Solutions',
        'description': 'Find flats, apartments, and real estate in Dubai and RAK. Property solutions with local expertise and support.'
    },
    'offers/index.astro': {
        'h1': 'Current Offers & Price List – Equipment & Machinery Deals',
        'description': 'Browse current special offers and competitive pricing on powder coating equipment, CNC machines, and industrial machinery.'
    },
    'automated/index.astro': {
        'h1': 'Automated Powder Coating Line – Advanced Power & Free Systems',
        'description': 'Automated powder coating lines with advanced power and free conveyor systems. High-capacity, energy-efficient production equipment.'
    },
    'get-started-powder-coating/index.astro': {
        'h1': "Get Started With Powder Coating – Beginner's Guide & Equipment",
        'description': 'Everything you need to start a powder coating business or upgrade your existing system. Equipment, setup guide, and professional support included.'
    },
    'powder-coating-booth/index.astro': {
        'h1': 'Powder Coating Booth – Professional Spray Booths With Filter Systems',
        'description': 'Professional powder coating booths with advanced filter systems, low noise operation, and patented static loading technology.'
    },
    'powder-coating-oven/index.astro': {
        'h1': 'Powder Coating Oven – Tunnel & Batch Curing Furnaces',
        'description': 'Powder coating ovens including tunnel and batch models, automatic lines, perfect powder coverage, and energy-efficient curing.'
    },
    'mdf-powder-coating-line/index.astro': {
        'h1': 'MDF Wood Board Powder Coating – Revolutionary One-Stage Process',
        'description': 'MDF and wood board coating system with revolutionary one-stage process for high-efficiency powder coating on wood products.'
    },
    'powdercoat-aluminium-profiles/index.astro': {
        'h1': 'Aluminium Profiles Powder Coating – 6 Meter Profile Systems',
        'description': 'Specialized machinery for powder coating aluminium profiles up to 6 meters. 2000+ workpieces/day, runs 24/7 with custom power & free design.'
    },
    'enamel-powdercoat/index.astro': {
        'h1': 'Enamel Powder Coating – High-Efficiency Revolutionary Process',
        'description': 'Enamel powder coating system with revolutionary process, high efficiency, low maintenance, and complete startup support across GCC.'
    },
    'powder-coating-machine/index.astro': {
        'h1': 'Powder Coating Spray Guns – Patented Technology With 9 Patents',
        'description': 'Professional spray guns with 9 patents for perfect powder coating quality. Minimize powder loss, maximize efficiency, and reduce coating time.'
    },
    'heesemann-sander/index.astro': {
        'h1': 'Heesemann Sanding Machines – Professional Wood & Material Sanding',
        'description': 'Heesemann sanding and grinding machines for professional woodworking, material finishing, and industrial dust collection.'
    },
    'dust-collection/index.astro': {
        'h1': 'Dust Collection Systems – Industrial Air Filtration & Recovery',
        'description': 'Dust collection and air filtration systems for powder coating booths, woodworking, and industrial manufacturing with recovery options.'
    },
    'used-machines/index.astro': {
        'h1': 'Used Machines in UAE – Weekly Updated Stock & Refurbished Equipment',
        'description': 'Used CNC machines, powder coating equipment, and industrial machinery with weekly updates, Dubai/Sharjah storage, and refurbished options.'
    },
    'sliding-table-saw/index.astro': {
        'h1': 'Sliding Table Saw – Precision Wood Cutting Equipment',
        'description': 'Professional sliding table saws for precise woodworking, panel cutting, and industrial wood processing.'
    },
    'edge-banding/index.astro': {
        'h1': 'Edge Banding Machines – Woodworking Equipment for Panel Finishing',
        'description': 'Edge banding and panel finishing machinery for furniture production and woodworking with automatic feeding systems.'
    },
    'hot-pressing/index.astro': {
        'h1': 'Hot Press Machine – Wood & Panel Pressing Equipment',
        'description': 'Wood hot press and panel pressing equipment for furniture manufacturing, veneering, and industrial pressing applications.'
    },
    'cnc-router/index.astro': {
        'h1': 'CNC Router – Woodworking & Materials Processing',
        'description': 'CNC router machines for woodworking, sign making, and material processing with precision cutting and carving capabilities.'
    },
    'fiber-laser/index.astro': {
        'h1': 'Fiber Laser Cutting & Welding Machines – Industrial Laser Systems',
        'description': 'Fiber laser cutting and laser welding machines for sheet metal, industrial applications, 3D bevel head systems, and high-power production.'
    },
    'cnc-miling/index.astro': {
        'h1': 'CNC Milling Machines – VMC & Production Machining Centers',
        'description': 'CNC milling machines and machining centers for precision manufacturing, VMC options, and production metalworking.'
    },
    'coil-fed-fiber-laser-cutting-machine-uae/index.astro': {
        'h1': 'Fiber Laser Cutting Machines – Coil-Fed & High-Power Systems',
        'description': 'Coil-fed fiber laser cutting machines for high-volume metal cutting, industrial laser systems, and advanced industrial applications.'
    }
}

def update_page(filepath, metadata):
    """Update a single page file with metadata."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        match = re.match(r'^(---\n)(.*?)(\n---\n)(.*)', content, re.DOTALL)
        if not match:
            print(f"  ⚠️  Could not parse frontmatter in {filepath}")
            return False
        
        frontmatter_marker_start = match.group(1)
        frontmatter = match.group(2)
        frontmatter_marker_end = match.group(3)
        body = match.group(4)
        
        # Update title in frontmatter if needed (keep existing or use h1)
        if 'const title' not in frontmatter and 'title =' not in frontmatter:
            # Add title declaration if missing
            frontmatter = f"const title = \"{metadata['h1']}\";\n" + frontmatter
        
        # Update or add title in const title
        if 'const title' in frontmatter:
            frontmatter = re.sub(
                r'const title = ["\']([^"\']*)["\'];',
                f'const title = "{metadata["h1"]}";',
                frontmatter
            )
        
        # Create new content with proper H1 meta tag added if not present
        new_frontmatter = frontmatter.strip()
        
        # Add meta description if not already there
        if 'meta name="description"' not in body:
            # Insert meta tag at the beginning of body
            meta_tag = f'<meta name="description" content="{metadata["description"]}">\n'
            body = meta_tag + body
        
        new_content = f"{frontmatter_marker_start}{new_frontmatter}{frontmatter_marker_end}{body}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated {filepath}")
        return True
    
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    pages_dir = Path('src/pages')
    
    if not pages_dir.exists():
        print(f"❌ Directory not found: {pages_dir}")
        return
    
    print(f"Updating pages in {pages_dir}...\n")
    
    updated = 0
    for rel_path, metadata in page_metadata.items():
        filepath = pages_dir / rel_path
        if filepath.exists():
            if update_page(str(filepath), metadata):
                updated += 1
        else:
            print(f"⚠️  File not found: {filepath}")
    
    print(f"\n✅ Successfully updated {updated}/{len(page_metadata)} pages")

if __name__ == '__main__':
    main()
