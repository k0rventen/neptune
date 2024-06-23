import type { TableColumns } from "~/type";

export const useVulnerabilities = () => {
  const searchValue = ref("");
  const isTyping = ref();
  const queryParams = ref({
    severity_filter: undefined,
    active_filter: undefined,
  });
  const columns: TableColumns[] = [
    {
      name: "Active",
      key: "active",
    },
    {
      name: "CVE",
      key: "name",
    },
    {
      name: "Severity",
      key: "severity",
    },
    {
      name: "Source",
      key: "affected_package",
    },
    {
      name: "Related tags",
      key: "affected_images",
    },
    {
      name: "Notes",
      key: "notes",
    },
  ];

  const delaySearch = (value: string) => {
    clearTimeout(isTyping.value);
    isTyping.value = setTimeout(() => {
      searchValue.value = value;
    }, 500);
  };

  const fetchVulnerabilities = async ({ pageParam = 0 }) => {
    let url = `http://localhost:5000/api/vulnerabilities?page=${pageParam}&per_page=40`;

    Object.entries(queryParams.value).forEach(([key, value]) => {
      if (value) {
        url += `&${key}=${value}`;
      }
    });

    const res = await fetch(url);

    return res.json();
  };

  return {
    searchValue,
    delaySearch,
    queryParams,
    fetchVulnerabilities,
    columns,
  };
};
