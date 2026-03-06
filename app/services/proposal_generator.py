def generate_proposal(project_type: str, description: str):

    proposal = f"""
Hello,

Thank you for sharing your requirements regarding {project_type}.

Based on your project description:

{description}

Our team can design and deploy an AI-driven solution including:

• Automated lead qualification  
• Workflow automation pipelines  
• CRM integrations (HubSpot, Salesforce)  
• Scalable AI models for future expansion  

Estimated Timeline:
2–4 weeks depending on integration complexity.

Expected Outcome:
Higher lead conversion rates, automated client workflows, and improved operational efficiency.

Best regards  
AI Solutions Team
"""

    return proposal.strip()
