export const useCalcConverter = (size: number): string => {
  if (size / 1024 >= 1) {
    if (size / 1024 / 1024 >= 1) {
      if (size / 1024 / 1024 / 1024 >= 1) {
        return (size / 1024 / 1024 / 1024).toFixed(2) + " Go";
      } else {
        return (size / 1024 / 1024).toFixed(2) + " Mo";
      }
    } else {
      return (size / 1024).toFixed(2) + " Ko";
    }
  } else {
    return size + " o";
  }
};
