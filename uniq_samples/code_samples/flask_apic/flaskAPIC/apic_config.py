import os
APIC=os.getenv("APIC") or "sandboxapic.cisco.com"
APIC_USER=os.getenv("APIC_USER") or "devnetuser"
APIC_PASSWORD=os.getenv("APIC_PASSWORD") or "Cisco123!"