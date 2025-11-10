import asyncio
import json
from src.kafka.config import create_kafka_consumer
from src.event import (
    InventoryFailedEvent,
    InventoryReservedEvent,
    OrderCreatedEvent,
    OrderCancelledEvent,
)
from src.kafka.producer import publish_inventory_reserved, publish_inventory_failed
from sqlalchemy.orm import Session
from fastapi import Depends
from src.database import get_db
from src.repositories import product_repository, reserved_order_repository

from src.database import SessionLocal
from confluent_kafka import KafkaError

async def handle_order_created_event(
    event: OrderCreatedEvent
):
    db = SessionLocal()
    print(f"📥 Nhận OrderCreatedEvent: {event}")
    try:
        # Giả lập giữ hàng
        if product_repository.decrease_stock_if_available(
            event.product_id, event.quantity, db
        ):
            # Lưu thông tin đơn hàng đã giữ hàng
            reserved_order_repository.insert_if_not_exists(
                db, event.order_id, event.product_id, event.quantity
            )

            print(f"✅ Đã giữ hàng cho Order {event.order_id}")
            # Đừng flush ở đây - sẽ gây blocking
            await publish_inventory_reserved(
                InventoryReservedEvent(
                    order_id=event.order_id,
                    status="RESERVED",
                    message="Hàng đã được giữ thành công.",
                )
            )
        else:
            await publish_inventory_failed(
                InventoryFailedEvent(
                    order_id=event.order_id, 
                    status="FAILED", 
                    message="Không đủ hàng trong kho."
                )
            )
    except Exception as e:
        print(f"❌ Giữ hàng thất bại: {e}")
        await publish_inventory_failed(
            InventoryFailedEvent(
                order_id=event.order_id, status="FAILED", message=str(e)
            )
        )
    finally:
        db.close()


async def handle_order_cancelled_event(
    event: OrderCancelledEvent
):
    db = SessionLocal()
    print(f"📥 Nhận OrderCancelledEvent: {event}")
    reserved_order = reserved_order_repository.get_by_order_id_and_product_id(
        db, event.order_id, event.product_id
    )
    if reserved_order:
        # Hoàn trả hàng
        product_repository.increase_stock(db, event.product_id, reserved_order.quantity)
        reserved_order_repository.delete_reserved_order(db, event.order_id, event.product_id)
        print(f"✅ Đã hoàn trả hàng cho Order {event.order_id}")
    db.close()

async def consume_orders():
    consumer = await asyncio.to_thread(create_kafka_consumer, ["orders"])
    try:
        while True:
            # Poll với timeout ngắn
            msg = await asyncio.to_thread(consumer.poll, 0.1) # 100ms timeout
            if msg is None:
                # Bạn không cần sleep nữa, vì poll đã "chờ" 0.1s rồi
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f"Kafka error: {msg.error()}")
                continue
            
            try:
                payload = json.loads(msg.value().decode("utf-8"))
                event = OrderCreatedEvent(**payload)
                # Chạy handler trong background, 
                # create_task để xử lý, không await ở đây
                asyncio.create_task(handle_order_created_event(event))
            except Exception as e:
                print(f"⚠️ Error processing orders message: {e}")
    except asyncio.CancelledError:
        print("📪 Stopping orders consumer")
    finally:
        # 3. Chạy hàm blocking close trong thread
        await asyncio.to_thread(consumer.close)

async def consume_orders_cancelled():
    consumer = await asyncio.to_thread(create_kafka_consumer, ["orders_cancelled"])
    try:
        while True:
            msg = await asyncio.to_thread(consumer.poll, 0.1)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f"Kafka error: {msg.error()}")
                continue
            
            try:
                payload = json.loads(msg.value().decode("utf-8"))
                event = OrderCancelledEvent(**payload)
                # Chạy handler trong background
                 # create_task để xử lý, không await ở đây
                asyncio.create_task(handle_order_cancelled_event(event))
            except Exception as e:
                print(f"⚠️ Error processing cancelled orders message: {e}")
    except asyncio.CancelledError:
        print("📪 Stopping cancelled orders consumer")
    finally:
        await asyncio.to_thread(consumer.close)

async def start_kafka_consumers():
    print("🚀 Starting Kafka consumers...")
    # Chạy consumers trong background
    await asyncio.gather(
        consume_orders(),
        consume_orders_cancelled(),
        return_exceptions=True
    )

# async def start_kafka_consumers():
#     consumer_orders = create_kafka_consumer(["orders"])
#     consumer_cancelled = create_kafka_consumer(["orders_cancelled"])

    

#     async def poll_consumer(consumer, handler, model_cls):
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 await asyncio.sleep(0.1)
#                 continue
#             if msg.error():
#                 print(f"Kafka error: {msg.error()}")
#                 continue
#             try:
#                 payload = json.loads(msg.value().decode("utf-8"))
#                 event = model_cls(**payload)
#                 db = SessionLocal()
#                 try:
#                     await handler(event, db=db)
#                 finally:
#                     db.close()
#             except Exception as e:
#                 print(f"⚠️ Error processing message: {e}")


#     await asyncio.gather(
#         poll_consumer(consumer_orders, handle_order_created_event, OrderCreatedEvent),
#         poll_consumer(
#             consumer_cancelled, handle_order_cancelled_event, OrderCancelledEvent
#         ),
#     )
