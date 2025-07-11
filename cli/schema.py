from datetime import datetime
from enum import Enum
from textwrap import dedent
from typing import Any

from pydantic import BaseModel, Field, model_validator


# Core objects
class JobStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    FAILED = 'failed'


class HonulabsOrganisation(BaseModel):
    org_id: str
    domain_id: str


class HonulabsBusiness(BaseModel):
    org: HonulabsOrganisation
    name: str
    business_id: str
    model_ref: str

class HonulabsBusinessPick(BaseModel):
    id: str
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


class BusinessPlanRequirementsCreate(BaseModel):
    idea: str = Field(
        ...,
        description='Detailed description of the idea for your new Saas product:',
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
        return dedent(f"""- {self.model_fields["inspiration"].description}
{self.inspiration}

- {self.model_fields["long_term_goals"].description}
{self.long_term_goals}

- {self.model_fields["brand_interpretation"].description}
{self.brand_interpretation}

- {self.model_fields["risk_assessment"].description}
{self.risk_assessment}""".strip())


class FullBusinessDetailsCreate(BaseModel):
    business_name: str
    # business_url: str  # ignored for now, using name.honulabs.xyz
    base_business_plan: BusinessPlan


class VercelSecrets(BaseModel):
    secrets: dict[str, Any]


class Collaborator(BaseModel):
    username: str


class Collaborators(BaseModel):
    collaborators: list[Collaborator]


class MarketSegment(BaseModel):
    core_market: str
    sub_category: str
    niche: str


class TokenSet(BaseModel):
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str