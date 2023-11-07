export const useBaseAPI = (request: any, opts: any) => {
    const config = useRuntimeConfig()


    return useFetch(request, {
        baseURL: config.public.apiBase, 
        ...opts
    })
}
