import en from '@/locales/en.json'
import fr from '@/locales/fr.json'
import it from '@/locales/it.json'

export default defineI18nConfig(() => ({
    legacy: false,
    messages: {
        en,
        fr,
        it
    }
}))