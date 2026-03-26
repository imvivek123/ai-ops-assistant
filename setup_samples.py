"""Setup script - Create sample data files"""

from pathlib import Path


def create_sample_data():
    """Create realistic sample data for testing"""
    
    # Create outputs directory
    Path("outputs").mkdir(exist_ok=True)
    
    # Create sample_data directory
    sample_dir = Path("sample_data")
    sample_dir.mkdir(exist_ok=True)
    
    # Meeting transcript
    meeting_transcript = """QUARTERLY BUSINESS REVIEW - Q1 2024
Meeting Date: March 22, 2024
Attendees: Sarah Chen (CEO), Michael Rodriguez (VP Sales), Emily Park (CFO), David Liu (CTO), Jessica Brown (Marketing Director)

---

Sarah Chen (CEO): Good morning everyone. Let's review our Q1 performance. Michael, sales metrics?

Michael Rodriguez (VP Sales): Absolutely. Q1 exceeded expectations. We closed $4.2M in new revenue, a 32% increase over Q4. Our top performer was the Tech sector with $1.8M. We acquired 47 new enterprise clients. However, government sector cycles are longer at 120 days.

Emily Park (CFO): Michael, what's the expected ROI? Each gov account averages $150K ARR.

Michael Rodriguez: With our current close rates, we'd expect 8-10 new gov accounts by end of Q2. That's roughly $1.2-1.5M additional revenue.

Emily Park: That math works. I can approve $180K for two senior AE hires.

David Liu (CTO): Cloud migration complete! Final cost: $280K vs $320K budgeted. We're saving approximately $8K/month on infrastructure going forward.

Sarah Chen: David, impressive. What about predictive analytics?

David Liu: Currently 65% complete. We're on track for beta release by mid-April.

Jessica Brown (Marketing Director): Perfect timing. We're planning a May launch event. I need $50K for conferences and content.

Sarah Chen: Jessica, what's the ROI? Conferences generated 23 leads last year, 5 closed. That's a 22% conversion rate. Approved.

Emily Park: Q2 cash flow concerns - $2.1M in bank, $1.8M in payables. No other major hires until Q2 revenues come in.

Sarah Chen: Michael, no new hires beyond the two positions. Key action items:

Michael Rodriguez: Hire two gov-focused AEs by April 15.

David Liu: Beta release by April 15.

Jessica Brown: Launch event May 3rd.

Sarah Chen: My items: (1) Board update on gov strategy by April 5, (2) Approve product roadmap, (3) Strategy session with Emily on unit economics by April 10.

Emily Park: Freezing discretionary spending except approved hires and marketing. Let's reconvene in two weeks. Good work this quarter, team."""
    
    (sample_dir / "meeting_transcript.txt").write_text(meeting_transcript, encoding='utf-8')
    print("✓ Created meeting_transcript.txt")
    
    # Sales data CSV
    sales_data = """Date,Region,Product,Units_Sold,Revenue,Customer_Segment,Sales_Rep,Quarter
2024-01-05,APAC,CloudPlatform,150,75000,Enterprise,Alice Johnson,Q1
2024-01-12,EMEA,Analytics,200,85000,SMB,Bob Smith,Q1
2024-01-19,AMER,CloudPlatform,180,90000,Enterprise,Carol Williams,Q1
2024-01-26,APAC,Integration,120,48000,Mid-Market,David Lee,Q1
2024-02-02,EMEA,Security,250,125000,Enterprise,Emma Davis,Q1
2024-02-09,AMER,Analytics,160,68000,SMB,Frank Brown,Q1
2024-02-16,APAC,CloudPlatform,190,95000,Enterprise,Grace Park,Q1
2024-02-23,EMEA,Integration,140,56000,Mid-Market,Henry Martinez,Q1
2024-03-01,AMER,Security,220,110000,Enterprise,Isabella Rodriguez,Q1
2024-03-08,APAC,Analytics,170,72500,SMB,Jack Chen,Q1
2024-03-15,EMEA,CloudPlatform,210,105000,Enterprise,Karen Wilson,Q1
2024-03-22,AMER,Integration,130,52000,Mid-Market,Liam Sullivan,Q1
2024-03-29,APAC,Security,240,120000,Enterprise,Michelle Zhang,Q1
2024-01-10,EMEA,Analytics,185,78750,SMB,Nathan Taylor,Q1
2024-02-14,AMER,CloudPlatform,175,87500,Enterprise,Olivia Patel,Q1
2024-03-07,APAC,Integration,145,58000,Mid-Market,Patricia Jones,Q1
2024-01-24,EMEA,Security,260,130000,Enterprise,Quincy Anderson,Q1
2024-02-28,AMER,Analytics,155,66000,SMB,Rachel Moore,Q1
2024-03-13,APAC,CloudPlatform,200,100000,Enterprise,Samuel Jackson,Q1
2024-03-27,EMEA,Integration,135,54000,Mid-Market,Tanya White,Q1
"""
    
    (sample_dir / "sales_data.csv").write_text(sales_data, encoding='utf-8')
    print("✓ Created sales_data.csv")
    
    # Document request
    doc_request = """Q1 2024 Business Performance Report

Please generate a comprehensive business performance report for Q1 2024 that includes:

1. Executive summary of quarterly results
2. Key performance metrics and KPIs
3. Analysis of regional performance (APAC, EMEA, AMER)
4. Product performance breakdown
5. Sales team performance and recognition
6. Market trends and competitive analysis
7. Q2 forecast and growth projections
8. Strategic recommendations for improvement
9. Risk assessment and mitigation strategies
10. Appendix with detailed metrics and data tables

The report should be professional, data-driven, and suitable for presentation to the board of directors.
Format: Markdown with clear sections and subsections.
Target audience: C-level executives and board members.
"""
    
    (sample_dir / "doc_request.txt").write_text(doc_request, encoding='utf-8')
    print("✓ Created doc_request.txt")
    
    print("\n✓ Sample data files created successfully!")


if __name__ == "__main__":
    create_sample_data()
