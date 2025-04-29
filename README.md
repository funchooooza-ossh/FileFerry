                    +---------------------------+
                    |       Transport Layer      |
                    |     (FastAPI, DTOs, DI)     |
                    +-------------+--------------+
                                  |
                    +-------------v--------------+
                    |     Application Layer       |
                    | (UseCases + Adapters + UoW)  |
                    +-------------+--------------+
                                  |
                    +-------------v--------------+
                    |         Domain Layer        |
                    | (Entities, ValueObjects,    |
                    |  Policies, Domain Services) |
                    +-------------+--------------+
                                  |
          +----------+------------+-------------+-----------+
          |          |                          |           |
+---------v-+  +------v-------+        +---------v-+   +-----v-------+
| Postgres  |  | MinIO Storage|        | (Future)  |   | (Future)    |
| SQL Repo  |  | File Storage |        | MongoDB   |   | SFTP Client |
| Adapter   |  | Adapter      |        | Adapter   |   | Adapter     |
+-----------+  +--------------+        +-----------+   +------------+

