"""
Prediction Consumer - Listen for prediction tasks from RabbitMQ
"""
import json
import logging
from aio_pika import connect_robust, IncomingMessage
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.prediction import AQIPrediction
from app.utils.data_loader import load_air_quality_data

logger = logging.getLogger(__name__)


async def process_prediction_task(message: IncomingMessage):
    """
    Process prediction task from queue
    
    Args:
        message: RabbitMQ message
    """
    async with message.process():
        try:
            # Parse message
            body = json.loads(message.body.decode())
            task_id = body.get('task_id')
            prediction_type = body.get('data', {}).get('prediction_type', 'air_quality')
            location_id = body.get('data', {}).get('location_id')
            forecast_days = body.get('data', {}).get('forecast_days', 7)
            
            logger.info(f"Processing prediction task {task_id}: type={prediction_type}, location={location_id}")
            
            # Load historical data
            async with AsyncSessionLocal() as db:
                air_data = await load_air_quality_data(db, location_id=location_id, limit=100)
                
                if len(air_data) < 10:
                    logger.warning(f"Insufficient data for prediction task {task_id}: only {len(air_data)} records")
                    return
                
                # Run prediction
                predictor = AQIPrediction(forecast_days=forecast_days)
                predictor.fit(air_data)
                predictions = predictor.predict_future()
                
                logger.info(f"Prediction completed for task {task_id}: {len(predictions)} days forecasted")
                logger.info(f"Predictions: {predictions}")
                
                # TODO: Store results in database
                
        except Exception as e:
            logger.error(f"Error processing prediction task: {e}", exc_info=True)


async def start_prediction_consumer():
    """Start RabbitMQ consumer for prediction tasks"""
    try:
        connection = await connect_robust(settings.RABBITMQ_URL)
        channel = await connection.channel()
        
        # Declare exchange and queue
        exchange = await channel.declare_exchange('ai.tasks', 'direct', durable=True)
        queue = await channel.declare_queue('ai.prediction.queue', durable=True)
        await queue.bind(exchange, routing_key='ai.prediction')
        
        # Start consuming
        await queue.consume(process_prediction_task)
        
        logger.info("Prediction consumer started, waiting for tasks...")
        
        return connection
        
    except Exception as e:
        logger.error(f"Error starting prediction consumer: {e}", exc_info=True)
        raise

