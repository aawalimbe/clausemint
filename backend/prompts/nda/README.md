# NDA Generator Prompt System

This directory contains the comprehensive prompt system for generating professional Non-Disclosure Agreements (NDAs) in Clausemint.

## File Structure

```
nda/
├── README.md                    # This documentation file
├── system_prompt.txt           # Core system prompt with legal expertise
├── template_generator.txt      # Main template generation prompt
├── nda_types.txt              # Specialized prompts for different NDA types
├── clause_library.txt         # Comprehensive clause library
├── customization_prompt.txt   # Customization and validation prompt
└── base_prompt.txt           # Legacy base prompt (deprecated)
```

## Prompt System Overview

### 1. System Prompt (`system_prompt.txt`)
- **Purpose**: Defines the AI's role and expertise
- **Content**: Legal expertise, document structure requirements, legal standards
- **Usage**: Provides foundational context for all NDA generation

### 2. Template Generator (`template_generator.txt`)
- **Purpose**: Main prompt for generating complete NDA documents
- **Content**: Document generation process, input parameters, output requirements
- **Usage**: Primary prompt used by the NDA generator

### 3. NDA Types (`nda_types.txt`)
- **Purpose**: Specialized guidance for different types of NDAs
- **Content**: Requirements for mutual, unilateral, employee, vendor, investment, joint venture, and technology NDAs
- **Usage**: Provides context-specific guidance based on NDA type

### 4. Clause Library (`clause_library.txt`)
- **Purpose**: Comprehensive collection of legal clauses
- **Content**: Standard and enhanced versions of all major NDA clauses
- **Usage**: Reference library for clause selection and customization

### 5. Customization Prompt (`customization_prompt.txt`)
- **Purpose**: Document review, customization, and validation
- **Content**: Validation checklist, customization tasks, compliance requirements
- **Usage**: For post-generation review and customization

## NDA Types Supported

### 1. Mutual NDA (Two-Way)
- Both parties disclose confidential information
- Equal obligations for both parties
- Balanced protection and restrictions

### 2. Unilateral NDA (One-Way)
- Only one party discloses confidential information
- Recipient has primary obligations
- Discloser has limited obligations

### 3. Employee NDA
- Employee-specific obligations
- Post-employment restrictions
- Work product ownership

### 4. Vendor/Supplier NDA
- Vendor access to company information
- Service-specific limitations
- Subcontractor restrictions

### 5. Investment NDA
- Due diligence context
- Financial information protection
- Deal-specific confidentiality

### 6. Joint Venture NDA
- Collaborative development context
- Shared IP considerations
- Joint ownership provisions

### 7. Technology/Startup NDA
- IP-heavy focus
- Patent and trade secret protection
- Innovation ownership

## Jurisdiction Support

### India (Common Law) - Default
- Indian Contract Act, 1872 compliance
- Information Technology Act, 2000 considerations
- Personal Data Protection Bill requirements
- Arbitration and Conciliation Act, 1996
- Indian court jurisdiction and enforcement
- Specific performance under Indian law
- Limitation Act, 1963 considerations

### US (Common Law)
- State-specific variations
- Trade secret protection
- Injunctive relief provisions

### EU (Civil Law)
- GDPR compliance
- Data protection requirements
- Cross-border considerations

### UK (Common Law)
- English law provisions
- UK-specific IP protection
- Brexit considerations

### International
- Choice of law provisions
- Dispute resolution mechanisms
- Cross-border enforcement

## Document Structure

Every generated NDA includes:

1. **Header Section**: Document title, date, party identification
2. **Recitals**: Purpose and context of the agreement
3. **Definitions**: Clear definition of confidential information and key terms
4. **Confidentiality Obligations**: Detailed non-disclosure requirements
5. **Permitted Disclosures**: Exceptions and authorized disclosures
6. **Term and Termination**: Duration and termination conditions
7. **Return of Materials**: Obligations upon termination
8. **Remedies and Enforcement**: Legal remedies for breaches
9. **General Provisions**: Standard contract terms
10. **Signature Blocks**: Proper execution format

## Input Parameters

The system accepts the following parameters:

- `{party_a}`: First party name and details
- `{party_b}`: Second party name and details
- `{party_c}`: Third party name and details (if applicable)
- `{nda_type}`: Type of NDA (mutual, unilateral, employee, etc.)
- `{purpose}`: Specific purpose of the NDA
- `{confidentiality_period}`: Duration of confidentiality obligations
- `{jurisdiction}`: Governing law and jurisdiction

## Usage

### Basic Generation
The system automatically uses the comprehensive prompt when generating NDAs through the API.

### Customization
To customize generated NDAs:
1. Use the customization prompt for review
2. Apply industry-specific adaptations
3. Validate jurisdiction compliance
4. Ensure all legal requirements are met

### Validation
The system includes comprehensive validation:
- Legal compliance checks
- Document structure validation
- Content accuracy verification
- Risk assessment

## Legal Disclaimer

This prompt system is designed to assist in generating NDA templates. However:
- Generated documents should be reviewed by qualified legal counsel
- Jurisdiction-specific requirements may vary
- Legal standards and requirements change over time
- The system does not constitute legal advice

## Maintenance

### Updating Prompts
- Review and update prompts regularly
- Monitor changes in legal requirements
- Update jurisdiction-specific content
- Maintain clause library currency

### Adding New NDA Types
1. Add type-specific requirements to `nda_types.txt`
2. Update `template_generator.txt` with new type handling
3. Add relevant clauses to `clause_library.txt`
4. Update this README with new type documentation

### Jurisdiction Updates
1. Monitor legal changes in supported jurisdictions
2. Update jurisdiction-specific content
3. Add new jurisdictions as needed
4. Maintain compliance with current legal standards 