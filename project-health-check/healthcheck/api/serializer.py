from rest_framework import serializers
from healthcheck.models import ServerHealthLog, ServerDetails, ServerMonitoringConfig
from django.contrib.auth import authenticate


class ServerHealthLogSerializer(serializers.ModelSerializer):
    """Serializer for ServerHealthLog Model"""

    ip_address = serializers.IPAddressField(write_only=True)
    health_status = serializers.CharField(required=False)

    class Meta:
        model = ServerHealthLog
        fields = [
            "ip_address",
            "cpu_usage_percent",
            "memory_usage_percent",
            "disk_usage_percent",
            "health_status",
        ]

        read_only_fields = [
            "created_at",
            "created_by",
            "updated_at",
        ]

    # def create(self, validated_data):
    #     ip_address = validated_data.pop("ip_address")
    #     server = ServerDetails.objects.filter(ip_address=ip_address).first()
    #     if server:
    #         validated_data["server"] = server
    #     else:
    #         raise serializers.ValidationError("Server IP not found!")

    #     cpu = validated_data.get("cpu_usage_percent", 0)
    #     memory = validated_data.get("memory_usage_percent", 0)
    #     disk = validated_data.get("disk_usage_percent", 0)

    #     custom_monitoring = ServerMonitoringConfig.objects.filter(
    #         server__ip_address=ip_address
    #     ).first()
    #     custom_metric_status = None
    #     if custom_monitoring:
    #         cpu_threshold = custom_monitoring.cpu_threshold_percent
    #         memory_threshold = custom_monitoring.memory_threshold_percent
    #         disk_threshold_percent = custom_monitoring.disk_threshold_percent

    #         if (
    #             cpu > cpu_threshold
    #             or memory > memory_threshold
    #             or disk > disk_threshold_percent
    #         ):
    #             custom_metric_status = ServerHealthLog.HealthStatus.WARNING
    #         else:
    #             custom_metric_status = ServerHealthLog.HealthStatus.HEALTHY
    #     else:
    #         # if not custom_monitoring:
    #         max_usage = max(cpu, memory, disk)

    #         # Determine Status
    #         if max_usage > 90:
    #             status = ServerHealthLog.HealthStatus.CRITICAL
    #         elif max_usage >= 80:
    #             status = ServerHealthLog.HealthStatus.WARNING
    #         else:
    #             status = ServerHealthLog.HealthStatus.HEALTHY
    #     validated_data["health_status"] = (
    #         custom_metric_status if custom_metric_status else status
    #     )

    #     if validated_data["health_status"] in [
    #         ServerHealthLog.HealthStatus.WARNING,
    #         ServerHealthLog.HealthStatus.CRITICAL,
    #     ]:
    #         validated_data["error_message"] = (
    #             f"🚨 Server Health Alert\n\n"
    #             f"Server IP: {ip_address}\n"
    #             f"CPU Usage: {cpu}%\n"
    #             f"Memory Usage: {memory}%\n"
    #             f"Disk Usage: {disk}%\n\n"
    #             f"Status: {validated_data['health_status'].label}\n\n"
    #             "One or more metrics have exceeded the configured threshold. "
    #             "Please investigate immediately."
    #         )
    #     return super().create(validated_data)

    def create(self, validated_data):
        ip_address = validated_data.pop("ip_address")

        server = ServerDetails.objects.filter(ip_address=ip_address).first()
        if not server:
            raise serializers.ValidationError("Server IP not found!")

        validated_data["server"] = server

        cpu = validated_data.get("cpu_usage_percent", 0)
        memory = validated_data.get("memory_usage_percent", 0)
        disk = validated_data.get("disk_usage_percent", 0)

        custom_monitoring = ServerMonitoringConfig.objects.filter(
            server__ip_address=ip_address
        ).first()

        custom_metric_status = None

        if custom_monitoring:
            cpu_threshold = custom_monitoring.cpu_threshold_percent
            memory_threshold = custom_monitoring.memory_threshold_percent
            disk_threshold = custom_monitoring.disk_threshold_percent

            if (
                cpu > cpu_threshold
                or memory > memory_threshold
                or disk > disk_threshold
            ):
                custom_metric_status = ServerHealthLog.HealthStatus.WARNING
            else:
                custom_metric_status = ServerHealthLog.HealthStatus.HEALTHY

        else:
            max_usage = max(cpu, memory, disk)

            if max_usage > 90:
                status = ServerHealthLog.HealthStatus.CRITICAL
            elif max_usage >= 80:
                status = ServerHealthLog.HealthStatus.WARNING
            else:
                status = ServerHealthLog.HealthStatus.HEALTHY

        new_status = custom_metric_status if custom_metric_status else status
        validated_data["health_status"] = new_status

        # Alert message
        if new_status in [
            ServerHealthLog.HealthStatus.WARNING,
            ServerHealthLog.HealthStatus.CRITICAL,
        ]:
            validated_data["error_message"] = (
                f"🚨 Server Health Alert\n\n"
                f"Server IP: {ip_address}\n"
                f"CPU Usage: {cpu}%\n"
                f"Memory Usage: {memory}%\n"
                f"Disk Usage: {disk}%\n\n"
                f"Status: {new_status.label}\n\n"
                "One or more metrics exceeded the configured threshold."
            )

        # ===============================
        # CHECK LAST LOG
        # ===============================

        last_log = (
            ServerHealthLog.objects.filter(server=server)
            .order_by("-created_at")
            .first()
        )

        if last_log and last_log.health_status == new_status:
            # UPDATE existing log
            last_log.cpu_usage_percent = cpu
            last_log.memory_usage_percent = memory
            last_log.disk_usage_percent = disk
            last_log.error_message = validated_data.get("error_message")
            last_log.save()

            return last_log

        # STATUS CHANGED → CREATE NEW ENTRY
        return super().create(validated_data)


class AgentAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError({"credentials": "Incorrect credentials"})

        if not user.is_active:
            raise serializers.ValidationError(
                {"credentials": "User account is inactive"}
            )

        return user
