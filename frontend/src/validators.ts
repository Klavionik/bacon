import * as validators from "@vuelidate/validators"

const validationMessages = {
  required: "Обязательное поле",
  requiredIf: "Обязательное поле",
  email: "Некорректный email",
  minLength: "Поле должно быть не короче {min} символов",
  sameAs: "Значения должны совпадать",
}

type Messages = {
  required: string
  requiredIf: string
  email: string
  minLength: string
  sameAs: string
}

type MessageParams = {
  [p: string]: any
  model: string
  property: string
}

const replaceRegex = /{([^{}]+)}/g

function createT(messages: Messages): (path: string, obj: MessageParams) => string {
  return function (path: string, params: MessageParams): string {
    const validator = path.split(".")[1] as keyof Messages
    const message = messages[validator]
    // @ts-ignore
    return message.replace(replaceRegex, (keyExpr: string, key: string): string => {
      return params[key] || ""
    })
  }
}

const { createI18nMessage } = validators
const t = createT(validationMessages)

const withI18nMessage = createI18nMessage({ t })

const required = withI18nMessage(validators.required)
const email = withI18nMessage(validators.email)
const minLength = withI18nMessage(validators.minLength, { withArguments: true })
const sameAs = withI18nMessage(validators.sameAs, { withArguments: true })
const requiredIf = withI18nMessage(validators.requiredIf, { withArguments: true })

export { requiredIf, required, email, minLength, sameAs }
