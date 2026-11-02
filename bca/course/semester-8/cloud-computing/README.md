# Cloud Computing — BCA 451 (Semester VIII, 3 credits)

Cloud foundations and the NIST model; virtualization internals and containers; cloud storage, erasure coding, consistent hashing and quorums; cloud networking, VPC addressing, VXLAN and load balancing; microservices, Kubernetes, autoscaling and serverless queueing; cloud security, IAM and envelope encryption; cloud economics, SLA arithmetic and FinOps.

| Unit | Title | Hours |
|---|---|---|
| 1 | Cloud Foundations, the NIST Model, Service and Deployment Models | 5 |
| 2 | Virtualization Internals and Containers | 7 |
| 3 | Cloud Storage, Erasure Coding, Consistent Hashing and Quorums | 7 |
| 4 | Cloud Networking, VPC Addressing, VXLAN, Load Balancing and CDN | 6 |
| 5 | Microservices, Kubernetes, Autoscaling and Queueing Theory | 7 |
| 6 | Cloud Security, IAM Evaluation and Envelope Encryption | 6 |
| 7 | Cloud Economics, SLA Mathematics and FinOps | 7 |

## Verification

`bca/tools/check_cloud.py` plus `fill_script_outputs.py`: every Python block is executed and its output inserted; the checker recomputes each figure independently (exact fractions for erasure-coding durability and queueing, coreutils `sha256sum` for OCI digests, a linear-scan ring lookup for consistent hashing, integer bit arithmetic for CIDR membership, integer ceilings for the HPA formula) and `--verify` demands that every expected line and prose figure is present.

## Notes

Service names and limits (AWS, Azure, Google Cloud, Kubernetes defaults) are given from memory of public documentation and change often; confirm against current provider documentation before relying on them. Prices are illustrative. The envelope-encryption demonstration uses the `cryptography` package (AES-GCM) and prints only structural facts, never key material.
