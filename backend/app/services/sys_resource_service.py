from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sys_resource import SysResource
from app.repositories.sys_resource_repository import SysResourceRepository
from app.schemas.sys_resource import (
    SysResourceCreate,
    SysResourceUpdate,
    SysResourceResponse,
    SysResourceListRequest,
)
from app.schemas.common import PageResponse, DataResponse


class SysResourceService:
    """资源服务"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.resource_repo = SysResourceRepository(session)

    async def create_resource(self, request: SysResourceCreate) -> SysResourceResponse:
        """创建资源"""
        resource = SysResource(
            name=request.name,
            type=request.type,
            pid=request.pid,
            path=request.path,
            perm_code=request.perm_code,
            icon=request.icon,
            visible=request.visible,
            sort=request.sort,
            status=1,
        )
        resource = await self.resource_repo.create(resource)
        await self.session.commit()

        return SysResourceResponse.model_validate(resource)

    async def update_resource(self, request: SysResourceUpdate) -> bool:
        """更新资源"""
        update_data = request.model_dump(exclude={"id"})
        success = await self.resource_repo.update_resource(request.id, **update_data)
        await self.session.commit()
        return success

    async def delete_resource(self, resource_id: int) -> bool:
        """删除资源"""
        success = await self.resource_repo.delete_resource(resource_id)
        await self.session.commit()
        return success

    async def get_resource_list(
        self, request: SysResourceListRequest
    ) -> PageResponse[SysResourceResponse]:
        """获取资源列表"""
        offset = (request.page - 1) * request.size
        resources = await self.resource_repo.list_all(
            offset=offset, limit=request.size, name=request.name
        )
        total = len(resources)  # 简化处理，实际应该有单独的count方法

        return PageResponse(
            success=True,
            message="",
            data=[SysResourceResponse.model_validate(r) for r in resources],
            total=total,
            page=request.page,
            size=request.size,
        )

    async def get_menu_tree(self) -> DataResponse[list[SysResourceResponse]]:
        """获取菜单树"""
        resources = await self.resource_repo.list_menu_tree()
        return DataResponse(
            success=True, message="", data=[SysResourceResponse.model_validate(r) for r in resources]
        )
