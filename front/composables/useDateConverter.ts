export const useDateConverter = (date: any) => {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    }
    
    return new Date(date).toLocaleDateString('fr-FR', options)
}