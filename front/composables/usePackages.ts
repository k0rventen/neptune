import type { TableColumns } from "~/type";

export const usePackages = () => {
  const searchValue = ref<string>();
  const isTyping = ref();

  const queryParams = computed(() => {
    return {
      name_filter: searchValue.value,
      with_outdated_versions: "",
      with_vulnerable_versions: "",
      type_filter: "",
    };
  });

  const columns: TableColumns[] = [
    {
      name: "Name",
      key: "name",
    },
    {
      name: "Dependencies type",
      key: "type",
    },
    {
      name: "Date added",
      key: "date_added",
    },
    {
      name: "Versions",
      key: "versions",
    },
  ];

  const delaySearch = (value: string) => {
    clearTimeout(isTyping.value);
    isTyping.value = setTimeout(() => {
      searchValue.value = value;
    }, 500);
  };

  const fetchProjects = async ({ pageParam = 0 }) => {
    let url = `http://localhost:5000/api/packages?page=${pageParam}&per_page=40`;

    Object.entries(queryParams.value).forEach(([key, value]) => {
      if (value) {
        url += `&${key}=${value}`;
      }
    });

    const res = await fetch(url);

    return res.json();
  };

  return {
    fetchProjects,
    delaySearch,
    isTyping,
    columns,
    queryParams,
    searchValue,
  };
};
