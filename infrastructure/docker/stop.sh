#!/bin/bash

# GreenEduMap Docker Environment Stop Script
# Usage: ./stop.sh

echo "🛑 Stopping GreenEduMap Docker Environment..."
echo ""

docker-compose down

echo ""
echo "✅ All services stopped."
echo ""
echo "💡 Tips:"
echo "  - To remove volumes (delete data): docker-compose down -v"
echo "  - To restart: ./start.sh"
