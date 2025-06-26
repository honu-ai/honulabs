from datetime import datetime
from enum import Enum
from textwrap import dedent
from typing import Any

from pydantic import BaseModel, Field, model_validator

from common.identity.schema.api import UserSession


# Core objects
class JobStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    FAILED = 'failed'


class HonulabsOrganisation(BaseModel):
    org_id: str
    domain_id: str


class HonulabsSession(BaseModel):
    token: str
    user: UserSession
    org: HonulabsOrganisation


class HonulabsBusiness(BaseModel):
    org: HonulabsOrganisation
    name: str
    business_id: str
    model_ref: str


class HonulabsJob(BaseModel):
    job_id: str
    job_type: str
    business: HonulabsBusiness
    status: JobStatus
    message: str | None = None
    cost: float | None = None
    error: str | None = None
    result: dict | None = None
    started_at: datetime
    finished_at: datetime | None = None


# Structures for Responses
class BusinessProblemDefinition(BaseModel):
    """
    Model for business problem definition.
    """
    populated_problem_definition_framework: str
    problem_statement: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_problem_definition_framework and problem_statement
        fields contain more than 50 characters.
        """
        if self.populated_problem_definition_framework is None or len(self.populated_problem_definition_framework) < 50:
            raise ValueError("populated_problem_definition_framework must contain more than 50 characters.")
        if self.problem_statement is None or len(self.problem_statement) < 50:
            raise ValueError("problem_statement must contain more than 50 characters.")

        return self


class CompetitorAnalysis(BaseModel):
    """
    Model for competitor analysis.
    """
    populated_competitor_analysis_framework: str
    competitor_comparison_table: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_competitor_analysis_framework and competitor_comparison_table
        fields contain more than 50 characters.
        """
        if self.populated_competitor_analysis_framework is None or len(
                self.populated_competitor_analysis_framework) < 50:
            raise ValueError("populated_competitor_analysis_framework must contain more than 50 characters.")
        if self.competitor_comparison_table is None or len(self.competitor_comparison_table) < 50:
            raise ValueError("competitor_comparison_table must contain more than 50 characters.")

        return self


class TargetMarketAnalysis(BaseModel):
    """
    Model for target market analysis.
    """
    populated_target_market_definition_framework: str
    target_market_summary: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_target_market_definition_framework and target_market_summary
        fields contain more than 50 characters.
        """
        if self.populated_target_market_definition_framework is None or len(
                self.populated_target_market_definition_framework) < 50:
            raise ValueError("populated_target_market_definition_framework must contain more than 50 characters.")
        if self.target_market_summary is None or len(self.target_market_summary) < 50:
            raise ValueError("target_market_summary must contain more than 50 characters.")
        return self


class ICPUserResearch(BaseModel):
    """
    Model for ICP User research.
    """
    icp_research_findings: str
    identified_icps: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the icp_research_findings and identified_icps
        fields contain more than 50 characters.
        """
        if self.icp_research_findings is None or len(self.icp_research_findings) < 50:
            raise ValueError("icp_research_findings must contain more than 50 characters.")
        if self.identified_icps is None or len(self.identified_icps) < 50:
            raise ValueError("identified_icps must contain more than 50 characters.")
        return self


class UniqueValueProposition(BaseModel):
    """
    Model for unique value proposition.
    """
    populated_value_proposition_definition_framework: str
    value_proposition_statement: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_value_proposition_definition_framework and value_proposition_statement
        fields contain more than 50 characters.
        """
        if self.populated_value_proposition_definition_framework is None or len(
                self.populated_value_proposition_definition_framework) < 50:
            raise ValueError("populated_value_proposition_definition_framework must contain more than 50 characters.")
        if self.value_proposition_statement is None or len(self.value_proposition_statement) < 50:
            raise ValueError("value_proposition_statement must contain more than 50 characters.")
        return self


class PricingStrategy(BaseModel):
    """
    Model for pricing strategy.
    """
    populated_pricing_strategy_framework: str
    pricing_summary: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_pricing_strategy_framework and pricing_summary
        fields contain more than 50 characters.
        """
        if self.populated_pricing_strategy_framework is None or len(self.populated_pricing_strategy_framework) < 50:
            raise ValueError("populated_pricing_strategy_framework must contain more than 50 characters.")
        # Check pricing_summary length
        if self.pricing_summary is None or len(self.pricing_summary) < 50:
            raise ValueError("pricing_summary must contain more than 50 characters.")

        return self


class PositioningSummary(BaseModel):
    """
    Model for positioning summary.
    """
    populated_positioning_definition_framework: str
    positioning_summary: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_positioning_definition_framework and positioning_summary
        fields contain more than 50 characters.
        """
        if self.populated_positioning_definition_framework is None or len(
                self.populated_positioning_definition_framework) < 50:
            raise ValueError("populated_positioning_definition_framework must contain more than 50 characters.")
        if self.positioning_summary is None or len(self.positioning_summary) < 50:
            raise ValueError("positioning_summary must contain more than 50 characters.")
        return self


# Job-specific payloads
class BusinessPlanRequirements(BaseModel):
    business_idea: str
    questions_and_answers: str
    problem_definition: BusinessProblemDefinition
    competitor_analysis: CompetitorAnalysis
    target_market_analysis: TargetMarketAnalysis
    ideal_customer_profile_research: ICPUserResearch
    unique_value_proposition: UniqueValueProposition
    pricing_strategy: PricingStrategy
    positioning_summary: PositioningSummary


class BusinessPlan(BaseModel):
    """
    Business model summary.
    """
    business_plan: str = Field(
        ..., description="The detailed business plan covering all of the inputs."
    )
    business_plan_concise: str | None = Field(
        default=None, description="A concise version of the business plan."
    )


class BusinessNameWithDomain(BaseModel):
    business_name: str = Field(..., description="Suggested name of the business.")
    domain_name_options: list[str] = Field(..., description="Suggested domain names that work for the business name.")

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_business_names_domains_framework field
        contains more than 50 characters.
        """
        if self.business_name is None or len(self.business_name) < 3:
            raise ValueError(
                "business_name must contain more than 50 characters.")
        if self.domain_name_options is None or len(
                self.domain_name_options) < 1:
            raise ValueError(
                "domain_name_options must contain at least 1 domain name.")
        return self


class BusinessNamesDomains(BaseModel):
    """
    Model for business names and domains.
    """
    business_names_with_domains: list[BusinessNameWithDomain]

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that there are at least 5 business names with domains.
        """
        if len(self.business_names_with_domains) < 5:
            raise ValueError("business_names_with_domains must contain at least 5 business names.")
        return self


class Brand(BaseModel):
    """
    Model for brand.
    """
    populated_brand_framework: str
    brand_summary: str
    font_style: str
    tone_of_voice: str
    brand_colors: str

    @model_validator(mode='after')
    def check_fields(self):
        """
        Validate that the populated_brand_framework and brand_summary
        fields contain more than 50 characters.
        """
        if self.populated_brand_framework is None or len(self.populated_brand_framework) < 50:
            raise ValueError("populated_brand_framework must contain more than 50 characters.")
        if self.brand_summary is None or len(self.brand_summary) < 50:
            raise ValueError("brand_summary must contain more than 50 characters.")
        return self


class BusinessBrandComponents(BaseModel):
    business_name: str
    business_domain: str
    business_brand: Brand
    business_logo: str


class WebsiteComponents(BaseModel):
    landing_page_json: str
    privacy_policy: str
    terms_of_service: str


class PrivacyPolicyVariables(BaseModel):
    """
    Model for privacy policy input variables.
    """
    company_legal_name: str = Field(...,
                                    description="The legal name of the company. Use 'PLACEHOLDER_COMPANY_LEGAL_NAME' if cannot be determined.")
    company_website_url: str = Field(...,
                                     description="The URL of the company's website. Use 'PLACEHOLDER_COMPANY_WEBSITE_URL' if cannot be determined.")
    company_name: str = Field(...,
                              description="The name of the company. Use 'PLACEHOLDER_COMPANY_NAME' if cannot be determined.")
    company_service_description: str = Field(...,
                                             description="A brief description of the services provided by the company. Use 'PLACEHOLDER_COMPANY_SERVICE_DESCRIPTION' if cannot be determined.")
    company_contact_email: str = Field(...,
                                       description="The contact email for the company. Use 'PLACEHOLDER_COMPANY_CONTACT_EMAIL' if cannot be determined.")
    ai_product_functions: str = Field(...,
                                      description="A brief description of the functions of the AI product. Use 'PLACEHOLDER_AI_PRODUCT_FUNCTIONS' if cannot be determined.")
    company_registered_address: str = Field(...,
                                            description="The registered address of the company. Use 'PLACEHOLDER_COMPANY_REGISTERED_ADDRESS' if cannot be determined.")


class TermsOfServiceVariables(BaseModel):
    """
    Model for terms of service input variables.
    """
    company_legal_name: str = Field(...,
                                    description="The legal name of the company. Use 'PLACEHOLDER_COMPANY_LEGAL_NAME' if cannot be determined.")
    country_of_company_registration: str = Field(...,
                                                 description="The country where the company is registered. Use 'PLACEHOLDER_COUNTRY_OF_COMPANY_REGISTRATION' if cannot be determined.")
    company_registration_address: str = Field(...,
                                              description="The registered address of the company. Use 'PLACEHOLDER_COMPANY_REGISTRATION_ADDRESS' if cannot be determined.")
    website_url: str = Field(...,
                             description="The URL of the company's website. Use 'PLACEHOLDER_WEBSITE_URL' if cannot be determined.")
    company_service_description: str = Field(...,
                                             description="A brief description of the services provided by the company. Use 'PLACEHOLDER_COMPANY_SERVICE_DESCRIPTION' if cannot be determined.")
    contact_email: str = Field(...,
                               description="The contact email for the company. Use 'PLACEHOLDER_CONTACT_EMAIL' if cannot be determined.")
    trial_period: str = Field(...,
                              description="The duration of the trial period offered by the company. Use 'PLACEHOLDER_TRIAL_PERIOD' if cannot be determined.")
    privacy_policy: str = Field(...,
                                description="The URL of the company's privacy policy. Use 'PLACEHOLDER_PRIVACY_POLICY' if cannot be determined.")


class IndividualSprintPlan(BaseModel):
    sprint_plan: str


class SprintPlanCollection(BaseModel):
    individual_sprints: list[IndividualSprintPlan]


class StrategyPricingPlan(BaseModel):
    """ Model for individual pricing plans """
    name: str
    description: str
    unit_amount: float
    currency: str
    recurring_interval: str | None = Field(default=None)
    recurring_trial_period_days: str | None = Field(default=None)
    metadata: dict


class StrategyPricingPlanCollection(BaseModel):
    pricing_plans: list[StrategyPricingPlan]


class UserPersona(BaseModel):
    user_persona: str


class JobsToBeDone(BaseModel):
    """
    Model for jobs to be done.
    """
    jtbd: str


class UserJourneyMapping(BaseModel):
    """
    Model for user journey mapping.
    """
    user_journey_map: str


class UserJourneyFlow(BaseModel):
    """
    Model for user journey flow.
    """
    user_journey_flow: str


class MVPFramework(BaseModel):
    """
    Model for MVP framework.
    """
    mvp: str


class ProductIntegration(BaseModel):
    service: str
    purpose: str
    manual_steps: list[str]
    programmatic_steps: list[str]


class ProductIntegrations(BaseModel):
    """
    Model for product integrations.
    """
    integrations: list[ProductIntegration]


class BusinessSpecifications(BaseModel):
    project_name: str
    project_domain: str
    landing_page_content: dict
    privacy_policy: str
    terms_of_service: str
    sprint_plans: list[str]
    github_repo_url: str | None
    supabase_project_id: str | None
    vercel_project_id: str | None


# Post Payloads
class HonulabsBusinessCreate(BaseModel):
    name: str


class BusinessPlanRequirementsCreate(BaseModel):
    idea: str = Field(
        ...,
        description='Detailed description of the idea for your new Saas product.',
    )
    inspiration: str = Field(
        ...,
        description='What inspired you to pursue this SaaS idea?',
    )
    long_term_goals: str = Field(
        ...,
        description='What long-term goals do you have for your Saas business?',
    )
    brand_interpretation: str = Field(
        ...,
        description='How do you want your customers to feel when interacting with your brand?',
    )
    risk_assessment: str = Field(
        ...,
        description='Are you willing to take calculated risks to achieve long-term goals, even if it means facing short-term uncertainties?',
    )

    @property
    def q_n_a(self) -> str:
        return dedent(f"""
        - {self.model_fields["inspiration"].description}
        {self.inspiration}

        - {self.model_fields["long_term_goals"].description}
        {self.long_term_goals}

        - {self.model_fields["brand_interpretation"].description}
        {self.brand_interpretation}

        - {self.model_fields["risk_assessment"].description}
        {self.risk_assessment}
        """.strip())


class FullBusinessDetailsCreate(BaseModel):
    business_name: str
    # business_url: str  # ignored for now, using name.honulabs.xyz
    base_business_plan: BusinessPlan


class VercelSecrets(BaseModel):
    secrets: dict[str, Any]
