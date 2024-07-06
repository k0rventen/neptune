import type { TableColumns } from "~/type";

export const useImage = () => {
  const columns: TableColumns[] = [
    {
      name: "Package",
      key: "package",
    },
    {
      name: "Version",
      key: "version",
    },
    {
      name: "Outdated",
      key: "outdated",
    },
  ];

  const activeVulnColumn: TableColumns[] = [
    {
      name: "Active",
      key: "active",
    },
    {
      name: "CVE",
      key: "name",
    },
    {
      name: "Affected package",
      key: "affected_package",
    },
    {
      name: "Severity",
      key: "severity",
    },
  ];

  return {
    columns,
    activeVulnColumn,
  };
};
