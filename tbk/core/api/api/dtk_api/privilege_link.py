from typing import Optional

from dtk_api import DtkAsyncApi
from dtk_api.gen import TbServiceGetPrivilegeLinkArgs, TbServiceGetPrivilegeLinkResp
from fastapi import Body
from fastapi import Depends
from pydantic import Field
from structlog.stdlib import BoundLogger

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.shared import AppErrno
from core.vendor.dtk import get_dtk_async
from ...api.app import app
from ...api_utils import api_inner_wrapper


class DtkPrivilegeLinkResponseModel(ResponseModel):
    data: Optional[TbServiceGetPrivilegeLinkResp] = Field(None, title="详细数据")


@app.post(
    "/dtk/privilege_link",
    tags=["大淘客"],
    summary="高效转链",
    description="",
    response_model=DtkPrivilegeLinkResponseModel,
)
async def dtk_privilege_link(
    args: TbServiceGetPrivilegeLinkArgs = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    dtk: DtkAsyncApi = Depends(get_dtk_async),
):
    @api_inner_wrapper(logger)
    async def inner():
        j = await dtk.tb_service_get_privilege_link(args)
        if j is None:
            return ApiResp.from_errno(AppErrno.dtk_error)
        return ApiResp.from_data(j)

    return await inner
