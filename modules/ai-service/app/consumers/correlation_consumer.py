"""
Correlation Consumer - Listen for correlation analysis tasks from RabbitMQ
"""
import json
import logging
from aio_pika import connect_robust, IncomingMessage
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.models.correlation import CorrelationAnalysis
from app.utils.data_loader import load_combined_data

logger = logging.getLogger(__name__)


async def process_correlation_task(message: IncomingMessage):
    """
    Process correlation analysis task from queue
    
    Args:
        message: RabbitMQ message
    """
    async with message.process():
        try:
            # Parse message
            body = json.loads(message.body.decode())
            task_id = body.get('task_id')
            analysis_type = body.get('data', {}).get('analysis_type', 'pearson')
            
            logger.info(f"Processing correlation task {task_id}: method={analysis_type}")
            
            # Load data
            async with AsyncSessionLocal() as db:
                combined_data = await load_combined_data(db)
                
                env_data = combined_data['environment']
                edu_data = combined_data['education']
                
                if len(env_data) < 3 or len(edu_data) < 3:
                    logger.warning(f"Insufficient data for correlation task {task_id}: env={len(env_data)}, edu={len(edu_data)}")
                    return
                
                # Run correlation analysis
                analyzer = CorrelationAnalysis(min_samples=3)  # Reduced for small dataset
                results = analyzer.analyze(env_data, edu_data, method=analysis_type)
                
                logger.info(f"Correlation analysis completed for task {task_id}")
                logger.info(f"Results: {results}")
                
                # Log insights
                for insight in results.get('insights', []):
                    logger.info(f"Insight: {insight}")
                
                # TODO: Store results in database
                
        except Exception as e:
            logger.error(f"Error processing correlation task: {e}", exc_info=True)


async def start_correlation_consumer():
    """Start RabbitMQ consumer for correlation tasks"""
    try:
        connection = await connect_robust(settings.RABBITMQ_URL)
        channel = await connection.channel()
        
        # Declare exchange and queue
        exchange = await channel.declare_exchange('ai.tasks', 'direct', durable=True)
        queue = await channel.declare_queue('ai.correlation.queue', durable=True)
        await queue.bind(exchange, routing_key='ai.correlation')
        
        # Start consuming
        await queue.consume(process_correlation_task)
        
        logger.info("Correlation consumer started, waiting for tasks...")
        
        return connection
        
    except Exception as e:
        logger.error(f"Error starting correlation consumer: {e}", exc_info=True)
        raise

