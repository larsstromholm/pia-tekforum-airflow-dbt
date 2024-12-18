from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
)

from dlt.common import jsonpath
from dlt.common.schema.typing import (
    TAnySchemaColumns,
    TColumnNames,
    TSchemaContract,
    TTableFormat,
    TWriteDispositionConfig,
)
from dlt.common.typing import TSortOrder
from dlt.extract.incremental.typing import LastValueFunc
from dlt.extract.items import TTableHintTemplate
from dlt.sources.helpers.rest_client.auth import AuthConfigBase, TApiKeyLocation
from dlt.sources.helpers.rest_client.paginators import (
    BasePaginator,
    HeaderLinkPaginator,
    JSONResponseCursorPaginator,
    OffsetPaginator,
    PageNumberPaginator,
    SinglePagePaginator,
)
from dlt.sources.helpers.rest_client.typing import HTTPMethodBasic

try:
    from dlt.sources.helpers.rest_client.paginators import JSONLinkPaginator
except ImportError:
    from dlt.sources.helpers.rest_client.paginators import (
        JSONResponsePaginator as JSONLinkPaginator,
    )

from dlt.sources.helpers.rest_client.auth import (
    APIKeyAuth,
    BearerTokenAuth,
    HttpBasicAuth,
)

PaginatorType = Literal[
    "json_link",
    "json_response",  # deprecated. Use json_link instead. Will be removed in upcoming release
    "header_link",
    "auto",
    "single_page",
    "cursor",
    "offset",
    "page_number",
]


class PaginatorTypeConfig(TypedDict, total=True):
    type: PaginatorType  # noqa


class PageNumberPaginatorConfig(PaginatorTypeConfig, total=False):
    """A paginator that uses page number-based pagination strategy."""

    base_page: Optional[int]
    page_param: Optional[str]
    total_path: Optional[jsonpath.TJsonPath]
    maximum_page: Optional[int]


class OffsetPaginatorConfig(PaginatorTypeConfig, total=False):
    """A paginator that uses offset-based pagination strategy."""

    limit: int
    offset: Optional[int]
    offset_param: Optional[str]
    limit_param: Optional[str]
    total_path: Optional[jsonpath.TJsonPath]
    maximum_offset: Optional[int]


class HeaderLinkPaginatorConfig(PaginatorTypeConfig, total=False):
    """A paginator that uses the 'Link' header in HTTP responses
    for pagination."""

    links_next_key: Optional[str]


class JSONLinkPaginatorConfig(PaginatorTypeConfig, total=False):
    """Locates the next page URL within the JSON response body. The key
    containing the URL can be specified using a JSON path."""

    next_url_path: Optional[jsonpath.TJsonPath]


class JSONResponseCursorPaginatorConfig(PaginatorTypeConfig, total=False):
    """Uses a cursor parameter for pagination, with the cursor value found in
    the JSON response body."""

    cursor_path: Optional[jsonpath.TJsonPath]
    cursor_param: Optional[str]


PaginatorConfig = Union[
    PaginatorType,
    PageNumberPaginatorConfig,
    OffsetPaginatorConfig,
    HeaderLinkPaginatorConfig,
    JSONLinkPaginatorConfig,
    JSONResponseCursorPaginatorConfig,
    BasePaginator,
    SinglePagePaginator,
    HeaderLinkPaginator,
    JSONLinkPaginator,
    JSONResponseCursorPaginator,
    OffsetPaginator,
    PageNumberPaginator,
]


AuthType = Literal["bearer", "api_key", "http_basic"]


class AuthTypeConfig(TypedDict, total=True):
    type: AuthType  # noqa


class BearerTokenAuthConfig(TypedDict, total=False):
    """Uses `token` for Bearer authentication in "Authorization" header."""

    # we allow for a shorthand form of bearer auth, without a type
    type: Optional[AuthType]  # noqa
    token: str


class ApiKeyAuthConfig(AuthTypeConfig, total=False):
    """Uses provided `api_key` to create authorization data in the specified `location` (query, param, header, cookie) under specified `name`"""

    name: Optional[str]
    api_key: str
    location: Optional[TApiKeyLocation]


class HttpBasicAuthConfig(AuthTypeConfig, total=True):
    """Uses HTTP basic authentication"""

    username: str
    password: str


# TODO: add later
# class OAuthJWTAuthConfig(AuthTypeConfig, total=True):


AuthConfig = Union[
    AuthConfigBase,
    AuthType,
    BearerTokenAuthConfig,
    ApiKeyAuthConfig,
    HttpBasicAuthConfig,
    BearerTokenAuth,
    APIKeyAuth,
    HttpBasicAuth,
]


class ClientConfig(TypedDict, total=False):
    base_url: str
    headers: Optional[Dict[str, str]]
    auth: Optional[AuthConfig]
    paginator: Optional[PaginatorConfig]


class IncrementalArgs(TypedDict, total=False):
    cursor_path: str
    initial_value: Optional[str]
    last_value_func: Optional[LastValueFunc[str]]
    primary_key: Optional[TTableHintTemplate[TColumnNames]]
    end_value: Optional[str]
    row_order: Optional[TSortOrder]
    convert: Optional[Callable[..., Any]]


class IncrementalConfig(IncrementalArgs, total=False):
    start_param: str
    end_param: Optional[str]


ParamBindType = Literal["resolve", "incremental"]


class ParamBindConfig(TypedDict):
    type: ParamBindType  # noqa


class ResolveParamConfig(ParamBindConfig):
    resource: str
    field: str


class IncrementalParamConfig(ParamBindConfig, IncrementalArgs):
    pass
    # TODO: implement param type to bind incremental to
    # param_type: Optional[Literal["start_param", "end_param"]]


@dataclass
class ResolvedParam:
    param_name: str
    resolve_config: ResolveParamConfig
    field_path: jsonpath.TJsonPath = field(init=False)

    def __post_init__(self) -> None:
        self.field_path = jsonpath.compile_path(self.resolve_config["field"])


class ResponseActionDict(TypedDict, total=False):
    status_code: Optional[Union[int, str]]
    content: Optional[str]
    action: Optional[Union[str, Union[Callable[..., Any], List[Callable[..., Any]]]]]


ResponseAction = Union[ResponseActionDict, Callable[..., Any]]


class Endpoint(TypedDict, total=False):
    path: Optional[str]
    method: Optional[HTTPMethodBasic]
    params: Optional[Dict[str, Union[ResolveParamConfig, IncrementalParamConfig, Any]]]
    json: Optional[Dict[str, Any]]
    paginator: Optional[PaginatorConfig]
    data_selector: Optional[jsonpath.TJsonPath]
    response_actions: Optional[List[ResponseAction]]
    incremental: Optional[IncrementalConfig]


class ProcessingSteps(TypedDict):
    filter: Optional[Callable[[Any], bool]]  # noqa: A003
    map: Optional[Callable[[Any], Any]]  # noqa: A003


class ResourceBase(TypedDict, total=False):
    """Defines hints that may be passed to `dlt.resource` decorator"""

    table_name: Optional[TTableHintTemplate[str]]
    max_table_nesting: Optional[int]
    write_disposition: Optional[TTableHintTemplate[TWriteDispositionConfig]]
    parent: Optional[TTableHintTemplate[str]]
    columns: Optional[TTableHintTemplate[TAnySchemaColumns]]
    primary_key: Optional[TTableHintTemplate[TColumnNames]]
    merge_key: Optional[TTableHintTemplate[TColumnNames]]
    schema_contract: Optional[TTableHintTemplate[TSchemaContract]]
    table_format: Optional[TTableHintTemplate[TTableFormat]]
    selected: Optional[bool]
    parallelized: Optional[bool]
    processing_steps: Optional[List[ProcessingSteps]]


class EndpointResourceBase(ResourceBase, total=False):
    endpoint: Optional[Union[str, Endpoint]]
    include_from_parent: Optional[List[str]]


class EndpointResource(EndpointResourceBase, total=False):
    name: TTableHintTemplate[str]


class RESTAPIConfig(TypedDict):
    client: ClientConfig
    resource_defaults: Optional[EndpointResourceBase]
    resources: List[Union[str, EndpointResource]]
