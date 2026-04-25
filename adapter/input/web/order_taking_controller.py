

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from adapter.input.web.validation_models.order_taking import CreateOrderInput
from adapter.out.persistance.repository import Repository
from application.domain.orderTaking.exceptions import OrderError
from application.domain.orderTaking.services.create_order_usecase import PlaceOrderUsecase
from application.port.incoming.interface_order_taking import CreateOrderDTO, CreateOrderLineDTO


router = APIRouter()

@router.post('/create_order')
async def create_order(create_order_input: CreateOrderInput):
    create_order_object = create_order_input.model_dump()
    order_lines_object = [CreateOrderLineDTO(**line) for line in create_order_object.pop("order_lines")]
    order_repository = Repository()
    place_order = PlaceOrderUsecase()
    order_dto = CreateOrderDTO(
        **create_order_object,
        order_lines=order_lines_object
    )

    try:
        created_order = await place_order.execute(order_dto, order_repository)
        return created_order
    except OrderError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})