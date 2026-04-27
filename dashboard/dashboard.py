import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# === PAGE CONFIG ===
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === LOAD DATA ===
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    main_df = pd.read_csv(os.path.join(base, 'main_data.csv'), parse_dates=['order_purchase_timestamp'])
    delivery_df = pd.read_csv(os.path.join(base, 'delivery_data.csv'), 
                               parse_dates=['order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date'])
    rfm_df = pd.read_csv(os.path.join(base, 'rfm_data.csv'))
    return main_df, delivery_df, rfm_df

main_df, delivery_df, rfm_df = load_data()

# === SIDEBAR ===
st.sidebar.image("https://img.icons8.com/color/96/000000/shopping-cart--v1.png", width=80)
st.sidebar.title("🛒 E-Commerce Dashboard")
st.sidebar.markdown("**Brazilian E-Commerce Public Dataset**")
st.sidebar.divider()

# Date filter
min_date = main_df['order_purchase_timestamp'].min().date()
max_date = main_df['order_purchase_timestamp'].max().date()

st.sidebar.subheader("📅 Filter Periode")
start_date = st.sidebar.date_input("Dari Tanggal", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Sampai Tanggal", value=max_date, min_value=min_date, max_value=max_date)

# Filter data
mask = (main_df['order_purchase_timestamp'].dt.date >= start_date) & \
       (main_df['order_purchase_timestamp'].dt.date <= end_date)
filtered_df = main_df[mask].copy()

st.sidebar.divider()
st.sidebar.markdown("**Dibuat untuk Proyek Akhir**")
st.sidebar.markdown("Dicoding Data Analysis Course")

# === MAIN CONTENT ===
st.title("🛒 E-Commerce Analytics Dashboard")
st.markdown(f"Data dari **{start_date}** hingga **{end_date}** | {len(filtered_df):,} transaksi")
st.divider()

# === KPI METRICS ===
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['total_payment'].sum()
total_orders = filtered_df['order_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
avg_review = filtered_df['review_score'].mean()

col1.metric("💰 Total Revenue", f"R$ {total_revenue:,.0f}", delta=None)
col2.metric("📦 Total Orders", f"{total_orders:,}", delta=None)
col3.metric("🧾 Avg Order Value", f"R$ {avg_order_value:,.1f}", delta=None)
col4.metric("⭐ Avg Review Score", f"{avg_review:.2f} / 5.0", delta=None)

st.divider()

# === TAB LAYOUT ===
tab1, tab2, tab3 = st.tabs(["📊 Analisis Kategori & Revenue", "🚚 Analisis Pengiriman", "👥 RFM Segmentation"])

# =====================
# TAB 1: CATEGORY & REVENUE
# =====================
with tab1:
    st.subheader("Pertanyaan 1: Kategori Produk & Tren Revenue Bulanan")
    st.markdown("> *Kategori produk apa yang menghasilkan total pendapatan tertinggi dan bagaimana tren penjualannya secara bulanan sepanjang periode 2017–2018?*")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🏆 Top Kategori Berdasarkan Revenue")
        top_n = st.slider("Tampilkan Top N Kategori", min_value=5, max_value=20, value=10, step=1)
        
        cat_rev = (filtered_df.groupby('product_category_name_english')['total_payment']
                   .sum().sort_values(ascending=False).head(top_n).reset_index())
        
        fig1, ax1 = plt.subplots(figsize=(6, top_n * 0.45 + 1))
        colors = sns.color_palette("Blues_d", top_n)
        bars = ax1.barh(cat_rev['product_category_name_english'][::-1], 
                        cat_rev['total_payment'][::-1] / 1e6, color=colors[::-1])
        ax1.set_xlabel('Total Revenue (Juta BRL)')
        ax1.set_title(f'Top {top_n} Kategori Produk')
        for bar, val in zip(bars, cat_rev['total_payment'][::-1]):
            ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                     f'{val/1e6:.1f}M', va='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

    with col_b:
        st.markdown("#### 📈 Tren Revenue Bulanan")
        monthly = (filtered_df.groupby('year_month')['total_payment']
                   .sum().reset_index().sort_values('year_month'))
        # Remove incomplete last month
        if len(monthly) > 1:
            monthly = monthly.iloc[:-1] if monthly.iloc[-1]['total_payment'] < monthly['total_payment'].mean() * 0.3 else monthly

        fig2, ax2 = plt.subplots(figsize=(6, 5))
        ax2.plot(range(len(monthly)), monthly['total_payment'] / 1e6, 
                 color='#1565C0', marker='o', linewidth=2.5, markersize=5)
        ax2.fill_between(range(len(monthly)), monthly['total_payment'] / 1e6, alpha=0.15, color='#1565C0')
        ax2.set_xticks(range(len(monthly)))
        ax2.set_xticklabels(monthly['year_month'], rotation=45, ha='right', fontsize=7)
        ax2.set_xlabel('Bulan')
        ax2.set_ylabel('Revenue (Juta BRL)')
        ax2.set_title('Tren Revenue Bulanan')
        
        # Annotate max
        max_idx = monthly['total_payment'].idxmax()
        max_pos = list(monthly.index).index(max_idx)
        ax2.annotate(f"Puncak\n{monthly.loc[max_idx,'year_month']}", 
                     xy=(max_pos, monthly.loc[max_idx,'total_payment']/1e6),
                     xytext=(max_pos - 2, monthly.loc[max_idx,'total_payment']/1e6 - 0.2),
                     arrowprops=dict(arrowstyle='->', color='red'), color='red', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # Insight box
    st.info("""**📌 Insight:**
- Kategori **health_beauty**, **watches_gifts**, dan **bed_bath_table** secara konsisten menjadi top kontributor revenue.
- Terdapat **lonjakan signifikan pada November 2017** yang berkorelasi dengan periode Black Friday/Harbolnas.
- Revenue menunjukkan tren **pertumbuhan positif** secara keseluruhan dari 2017 ke 2018.""")

    # Data table
    with st.expander("📋 Lihat Data Lengkap Kategori"):
        all_cat = (filtered_df.groupby('product_category_name_english')['total_payment']
                   .sum().sort_values(ascending=False).reset_index())
        all_cat.columns = ['Kategori', 'Total Revenue (BRL)']
        all_cat['Total Revenue (BRL)'] = all_cat['Total Revenue (BRL)'].map('R$ {:,.0f}'.format)
        st.dataframe(all_cat, use_container_width=True)

# =====================
# TAB 2: DELIVERY ANALYSIS
# =====================
with tab2:
    st.subheader("Pertanyaan 2: Performa Pengiriman per State")
    st.markdown("> *State mana yang memiliki performa pengiriman terburuk dan bagaimana distribusi waktu pengiriman di seluruh Brasil?*")

    # Filter delivery data to same period
    del_mask = (delivery_df['order_purchase_timestamp'].dt.date >= start_date) & \
               (delivery_df['order_purchase_timestamp'].dt.date <= end_date)
    del_filtered = delivery_df[del_mask].copy()
    del_filtered['on_time'] = del_filtered['order_delivered_customer_date'] <= del_filtered['order_estimated_delivery_date']

    state_stats = (del_filtered.groupby('customer_state')
                   .agg(
                       avg_days=('delivery_days', 'mean'),
                       median_days=('delivery_days', 'median'),
                       orders=('order_id', 'count'),
                       on_time_rate=('on_time', 'mean')
                   ).reset_index().sort_values('avg_days', ascending=False))

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("#### 🗺️ Rata-Rata Waktu Pengiriman per State")
        
        fig3, ax3 = plt.subplots(figsize=(6, 8))
        state_sorted = state_stats.sort_values('avg_days')
        palette = ['#ef5350' if v > 20 else '#ffca28' if v > 12 else '#66bb6a' for v in state_sorted['avg_days']]
        ax3.barh(state_sorted['customer_state'], state_sorted['avg_days'], color=palette)
        mean_days = state_stats['avg_days'].mean()
        ax3.axvline(x=mean_days, color='navy', linestyle='--', linewidth=1.5,
                    label=f'Rata-rata: {mean_days:.1f} hari')
        ax3.set_xlabel('Rata-Rata Hari Pengiriman')
        ax3.set_title('Waktu Pengiriman per State\n(🟢 <12 hari | 🟡 12-20 hari | 🔴 >20 hari)')
        ax3.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    with col_d:
        st.markdown("#### 📊 On-Time Rate vs Waktu Pengiriman")
        
        fig4, ax4 = plt.subplots(figsize=(6, 5))
        scatter = ax4.scatter(
            state_stats['avg_days'],
            state_stats['on_time_rate'] * 100,
            s=state_stats['orders'] / 20,
            alpha=0.7,
            c=state_stats['avg_days'],
            cmap='RdYlGn_r',
            edgecolors='gray',
            linewidth=0.5
        )
        plt.colorbar(scatter, ax=ax4, label='Avg Delivery Days')
        
        # Label worst/best
        for _, row in state_stats.head(5).iterrows():
            ax4.annotate(row['customer_state'],
                        (row['avg_days'], row['on_time_rate']*100),
                        textcoords='offset points', xytext=(4, 0), fontsize=8, color='red')
        for _, row in state_stats.tail(3).iterrows():
            ax4.annotate(row['customer_state'],
                        (row['avg_days'], row['on_time_rate']*100),
                        textcoords='offset points', xytext=(4, 0), fontsize=8, color='green')
        
        ax4.set_xlabel('Rata-Rata Hari Pengiriman')
        ax4.set_ylabel('On-Time Rate (%)')
        ax4.set_title('On-Time Rate vs Waktu Pengiriman\n(ukuran titik = jumlah order)')
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

        st.markdown("#### 📈 Distribusi Waktu Pengiriman")
        fig5, ax5 = plt.subplots(figsize=(6, 3.5))
        ax5.hist(del_filtered['delivery_days'].dropna(), bins=40, color='#1565C0', alpha=0.8, edgecolor='white')
        ax5.axvline(del_filtered['delivery_days'].mean(), color='red', linestyle='--',
                    label=f"Mean: {del_filtered['delivery_days'].mean():.1f} hari")
        ax5.axvline(del_filtered['delivery_days'].median(), color='orange', linestyle='--',
                    label=f"Median: {del_filtered['delivery_days'].median():.1f} hari")
        ax5.set_xlabel('Hari Pengiriman')
        ax5.set_ylabel('Frekuensi')
        ax5.set_title('Distribusi Waktu Pengiriman')
        ax5.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

    st.info(f"""**📌 Insight:**
- **On-time rate keseluruhan: {del_filtered['on_time'].mean()*100:.1f}%** — cukup baik secara nasional.
- State **RR, AP, AM** di wilayah utara Brasil memiliki rata-rata pengiriman >25 hari, hampir **2x lipat** rata-rata nasional ({del_filtered['delivery_days'].mean():.1f} hari).
- **SP (São Paulo)** dan **PR** adalah state terbaik, mencerminkan konsentrasi infrastruktur logistik di wilayah tenggara.""")

    with st.expander("📋 Lihat Tabel Lengkap per State"):
        state_display = state_stats.copy()
        state_display['avg_days'] = state_display['avg_days'].round(1)
        state_display['on_time_rate'] = (state_display['on_time_rate'] * 100).round(1).astype(str) + '%'
        state_display.columns = ['State', 'Avg Delivery Days', 'Median Days', 'Total Orders', 'On-Time Rate']
        st.dataframe(state_display, use_container_width=True)

# =====================
# TAB 3: RFM SEGMENTATION
# =====================
with tab3:
    st.subheader("Analisis Lanjutan: RFM Customer Segmentation")
    st.markdown("""
    RFM Analysis mengelompokkan pelanggan berdasarkan:
    - **R (Recency):** Berapa hari lalu terakhir berbelanja
    - **F (Frequency):** Berapa kali total transaksi
    - **M (Monetary):** Total nilai pembelian (BRL)
    """)

    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown("#### 🍩 Distribusi Segmen Pelanggan")
        segment_counts = rfm_df['Segment'].value_counts()
        colors_seg = ['#1976D2','#42A5F5','#90CAF9','#FFA726','#EF5350','#AB47BC'][:len(segment_counts)]
        
        fig6, ax6 = plt.subplots(figsize=(6, 5))
        wedges, texts, autotexts = ax6.pie(
            segment_counts.values, labels=segment_counts.index,
            autopct='%1.1f%%', colors=colors_seg, startangle=90, pctdistance=0.82
        )
        centre = plt.Circle((0,0), 0.55, fc='white')
        ax6.add_artist(centre)
        ax6.text(0, 0, f'{rfm_df.shape[0]:,}\nCustomers', ha='center', va='center', fontsize=10, fontweight='bold')
        ax6.set_title('Distribusi Segmen Pelanggan')
        plt.tight_layout()
        st.pyplot(fig6)
        plt.close()

    with col_f:
        st.markdown("#### 💰 Rata-Rata Monetary per Segmen")
        avg_monetary = rfm_df.groupby('Segment')['Monetary'].mean().sort_values()
        
        fig7, ax7 = plt.subplots(figsize=(6, 4))
        bar_colors = ['#1976D2' if v > avg_monetary.median() else '#90CAF9' for v in avg_monetary.values]
        bars = ax7.barh(avg_monetary.index, avg_monetary.values, color=bar_colors)
        ax7.set_xlabel('Rata-Rata Monetary (BRL)')
        ax7.set_title('Rata-Rata Nilai Pembelian per Segmen')
        for bar, val in zip(bars, avg_monetary.values):
            ax7.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                     f'R$ {val:.0f}', va='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig7)
        plt.close()

        st.markdown("#### 📊 Statistik RFM per Segmen")
        rfm_summary = rfm_df.groupby('Segment')[['Recency','Frequency','Monetary']].mean().round(1)
        rfm_summary['Jumlah Pelanggan'] = rfm_df['Segment'].value_counts()
        st.dataframe(rfm_summary, use_container_width=True)

    st.success("""**📌 Insight & Rekomendasi:**
- **Champions** & **Loyal Customers**: Berikan reward eksklusif & early access untuk mempertahankan mereka.
- **New Customers** (~besar): Kirim diskon follow-up untuk mendorong pembelian kedua.
- **At Risk**: Luncurkan win-back campaign dengan penawaran personal berbasis riwayat pembelian.
- **Others** (mayoritas): Fokus pada peningkatan repeat purchase melalui personalisasi rekomendasi produk.""")
