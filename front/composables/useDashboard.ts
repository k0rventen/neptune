import { useQuery } from "@tanstack/vue-query";
import type { StatType } from "~/type.d";

export const useDashboard = () => {
  const chartIndex = ref(0);

  const { data: current, isLoading: isLoadingStat } = useQuery({
    queryKey: ["current-stat"],
    queryFn: async () => {
      const res = await fetch(
        "http://localhost:5000/api/statistics?current=true"
      );
      return res.json();
    },
    staleTime: 60 * 1000 * 3,
  });

  const { data: recordStat, isLoading: isLoadingRecordStat } = useQuery({
    queryKey: ["historical-stat"],
    queryFn: async () => {
      const res = await fetch(
        "http://localhost:5000/api/statistics?current=false"
      );
      return res.json();
    },
    staleTime: 60 * 1000 * 3,
  });

  const { data: featured, isLoading: isLoadingFeatured } = useQuery({
    queryKey: ["featured"],
    queryFn: async () => {
      const res = await fetch("http://localhost:5000/api/tags/featured");
      return res.json();
    },
    staleTime: 60 * 1000 * 3,
  });

  const brandTextFeatured = (index: number): string => {
    const text = [
      "MOST ACTIVE VULN !",
      "MOST OUT. PACKAGES !",
      "MOST PACKAGE",
      "MOST RECENT",
      "MOST VULN",
    ];
    return text[index];
  };

  const isLoadingData = computed(() => {
    return (
      isLoadingStat.value ||
      isLoadingRecordStat.value ||
      isLoadingFeatured.value
    );
  });

  const graphTitle = computed(() => {
    switch (chartIndex.value) {
      case 0:
        return "Image tracking";
      case 1:
        return "Vulnerabilities tracking";
      case 2:
        return "Packages tracking";
    }
  });

  const changeGraph = (type: "left" | "right") => {
    if (type === "left") {
      if (chartIndex.value - 1 < 0) {
        chartIndex.value = 2;
      } else {
        chartIndex.value -= 1;
      }
    } else {
      if (chartIndex.value + 1 > 2) {
        chartIndex.value = 0;
      } else {
        chartIndex.value += 1;
      }
    }
  };

  const series = computed(() => {
    const data = [];

    switch (chartIndex.value) {
      case 0:
        data.push({
          name: "Total images",
          data: recordStat.value.map((stat: StatType) => stat.tags_total_count),
        });
        data.push({
          name: "Vulnerable images",
          data: recordStat.value.map(
            (stat: StatType) => stat.vulnerable_tags_count
          ),
        });
        data.push({
          name: "Images with outdated packages",
          data: recordStat.value.map(
            (stat: StatType) => stat.outdated_tags_count
          ),
        });
        break;
      case 1:
        data.push({
          name: "Total vulnerabilities",
          data: recordStat.value.map(
            (stat: StatType) => stat.vulnerabilities_total_count
          ),
        });
        data.push({
          name: "Active vulnerabilities",
          data: recordStat.value.map(
            (stat: StatType) => stat.active_vulnerabilities_count
          ),
        });
        data.push({
          name: "Low vulnerabilities",
          data: recordStat.value.map(
            (stat: StatType) => stat.low_vulnerabilities_count
          ),
        });
        data.push({
          name: "Medium vulnerabilities",
          data: recordStat.value.map(
            (stat: StatType) => stat.medium_vulnerabilities_count
          ),
        });
        data.push({
          name: "High vulnerabilities",
          data: recordStat.value.map(
            (stat: StatType) => stat.high_vulnerabilities_count
          ),
        });
        data.push({
          name: "Critical vulnerabilities",
          data: recordStat.value.map(
            (stat: StatType) => stat.critical_vulnerabilities_count
          ),
        });
        break;
      case 2:
        data.push({
          name: "Total packages",
          data: recordStat.value.map(
            (stat: StatType) => stat.packages_total_count
          ),
        });
        data.push({
          name: "Outdated packages",
          data: recordStat.value.map(
            (stat: StatType) => stat.outdated_packages_count
          ),
        });
        data.push({
          name: "Vulnerable packages",
          data: recordStat.value.map(
            (stat: StatType) => stat.vulnerable_packages_count
          ),
        });
        break;
    }

    return data;
  });

  return {
    isLoadingData,
    current,
    recordStat,
    featured,
    changeGraph,
    series,
    chartIndex,
    graphTitle,
    brandTextFeatured,
  };
};
