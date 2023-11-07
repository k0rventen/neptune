export const useColorSeverity = (item) => {
    switch (item.severity) {
        case 'Critical':
            return 'bg-black'
        case 'High':
            return 'bg-red-500'
        case 'Medium':
            return 'bg-yellow-500'
        case 'Low':
            return 'bg-green-600'
        case 'Negligible':
            return 'bg-[#A6D1E6]'
        case 'Unknown':
            return 'bg-[#eac7ff]'
    }
}
