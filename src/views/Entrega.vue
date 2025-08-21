<template>
  <form
    class="w-full flex flex-col justify-center items-center py-28 gap-10"
    @submit.prevent="submitForm"
  >
    <h2 class="font-bold text-3xl mb-8">Entrega</h2>

    <div class="flex flex-col gap-2 w-full max-w-md">
      <h3 class="font-semibold mb-2">Endereço</h3>

      <div class="flex flex-col">
        <div class="flex gap-2">
          <input
            v-model="form.cep"
            @input="onCepInput"
            @keypress="searchCep"
            placeholder="CEP*"
            class="border p-2 rounded w-8/12"
            :class="{ 'border-red-500': cepErro }"
            inputmode="numeric"
            autocomplete="on"
          />

          <button
            @click="searchCep"
            class="w-4/12 text-center bg-btn text-dark font-medium rounded border-2 border-dark cursor-pointer"
          >
            Buscar endereço
          </button>
        </div>
        <div class="text-sm mt-1">
          <span v-if="cepLoading" class="italic">Buscando endereço...</span>
          <span v-else-if="cepErro" class="text-red-500">{{ cepErro }}</span>
        </div>
      </div>

      <div class="flex gap-2">
        <input
          v-model="form.rua"
          placeholder="Rua*"
          class="border p-2 rounded w-9/12"
          :class="{ 'border-red-500': inputsErro && !form.rua }"
        />
        <input
          v-model="form.numero"
          placeholder="Número*"
          class="border p-2 rounded w-3/12"
          :class="{ 'border-red-500': inputsErro && !form.numero }"
        />
      </div>
      <input
        v-model="form.complemento"
        placeholder="Complemento (opcional)"
        class="border p-2 rounded"
      />
      <input
        v-model="form.bairro"
        placeholder="Bairro*"
        class="border p-2 rounded"
        :class="{ 'border-red-500': inputsErro && !form.bairro }"
      />
      <div class="flex gap-2">
        <input
          v-model="form.cidade"
          placeholder="Cidade*"
          class="border p-2 rounded w-9/12"
          :class="{ 'border-red-500': inputsErro && !form.cidade }"
        />
        <input
          v-model="form.estado"
          placeholder="Estado*"
          class="border p-2 rounded w-3/12"
          :class="{ 'border-red-500': inputsErro && !form.estado }"
        />
      </div>
      <input
        v-model="form.obs"
        placeholder="Observação (opcional)"
        class="border p-2 rounded"
      />
    </div>

    <div class="flex flex-col w-full max-w-md">
      <h3 class="font-semibold mb-4">Dados para Entrega</h3>
      <input
        v-model="form.nome"
        placeholder="Nome*"
        class="border p-2 rounded mb-2"
        :class="{ 'border-red-500': inputsErro && !form.nome }"
        autocomplete="on"
      />
      <input
        v-model="form.sobrenome"
        placeholder="Sobrenome"
        class="border p-2 rounded mb-2"
      />
      <input
        v-model="form.telefone"
        @input="onTelefoneInput"
        @blur="validarTelefone"
        placeholder="Telefone com DDD*"
        class="border p-2 rounded"
        :class="{ 'border-red-500': telefoneErro }"
        inputmode="tel"
        autocomplete="on"
        maxlength="15"
      />
      <div v-if="telefoneErro" class="text-red-500 text-sm mt-1">
        {{ telefoneErro }}
      </div>
    </div>

    <div class="flex flex-col w-full max-w-md">
      <h3 class="font-semibold mb-4">Dados para Nota Fiscal</h3>
      <input
        v-model="form.cpfCnpj"
        @input="onCpfCnpjInput"
        @blur="validarCpfCnpj"
        placeholder="CPF/CNPJ*"
        class="border p-2 rounded"
        :class="{ 'border-red-500': cpfCnpjErro }"
        inputmode="numeric"
        autocomplete="on"
        maxlength="18"
      />
      <div v-if="cpfCnpjErro" class="text-red-500 text-sm mt-1">
        {{ cpfCnpjErro }}
      </div>
    </div>

    <button
      type="submit"
      class="text-center px-10 py-4 text-xl bg-btn text-dark font-medium rounded-full border-2 border-dark cursor-pointer mt-8"
    >
      Ir para pagamento
    </button>

    <div v-if="mensagemErro" class="text-red-500 font-medium">
      {{ mensagemErro }}
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";

onMounted(() => {
  const salvo = localStorage.getItem("formEntrega");
  if (salvo) {
    const dados = JSON.parse(salvo);
    Object.assign(form, dados);
  }
});

const router = useRouter();

const form = reactive({
  nome: "",
  sobrenome: "",
  telefone: "",
  cep: "",
  rua: "",
  numero: "",
  complemento: "",
  bairro: "",
  cidade: "",
  estado: "",
  cpfCnpj: "",
  obs: "",
});

function limparNumero(valor) {
  return (valor || "").replace(/\D/g, "");
}

function isCpfCnpjValido(valor) {
  const num = limparNumero(valor);
  if (num.length === 11) return isCPFValido(num);
  if (num.length === 14) return isCNPJValido(num);
  return false;
}

function isCPFValido(cpf) {
  const n = limparNumero(cpf);
  if (n.length !== 11) return false;
  if (/^(\d)\1{10}$/.test(n)) return false;

  let soma = 0;
  for (let i = 0; i < 9; i++) soma += Number(n[i]) * (10 - i);
  let resto = soma % 11;
  const dv1 = resto < 2 ? 0 : 11 - resto;
  if (dv1 !== Number(n[9])) return false;

  soma = 0;
  for (let i = 0; i < 10; i++) soma += Number(n[i]) * (11 - i);
  resto = soma % 11;
  const dv2 = resto < 2 ? 0 : 11 - resto;

  return dv2 === Number(n[10]);
}

function isCNPJValido(cnpj) {
  const n = limparNumero(cnpj);
  if (n.length !== 14) return false;
  if (/^(\d)\1{13}$/.test(n)) return false;

  const pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
  const pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

  const calcDV = (base, pesos) => {
    const soma = base
      .split("")
      .reduce((acc, dig, i) => acc + Number(dig) * pesos[i], 0);
    const resto = soma % 11;
    return resto < 2 ? 0 : 11 - resto;
  };

  const dv1 = calcDV(n.slice(0, 12), pesos1);
  if (dv1 !== Number(n[12])) return false;

  const dv2 = calcDV(n.slice(0, 13), pesos2);
  return dv2 === Number(n[13]);
}

function isTelefoneValido(telefone) {
  const telLimpo = limparNumero(telefone);
  return /^(\d{10}|\d{11})$/.test(telLimpo);
}

function aplicarMascaraTelefone(valor) {
  const d = limparNumero(valor).slice(0, 11);
  if (d.length === 0) return "";
  if (d.length <= 2) return `(${d}`;
  if (d.length <= 6) return `(${d.slice(0, 2)}) ${d.slice(2)}`;
  if (d.length <= 10)
    return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
  return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
}

function onTelefoneInput(e) {
  form.telefone = aplicarMascaraTelefone(e.target.value);
  mensagemErro.value = "";
}

function aplicarMascaraCpf(cpf) {
  const d = limparNumero(cpf).slice(0, 11);
  if (d.length <= 3) return d;
  if (d.length <= 6) return `${d.slice(0, 3)}.${d.slice(3)}`;
  if (d.length <= 9) return `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6)}`;
  return `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6, 9)}-${d.slice(9)}`;
}

function aplicarMascaraCnpj(cnpj) {
  const d = limparNumero(cnpj).slice(0, 14);
  if (d.length <= 2) return d;
  if (d.length <= 5) return `${d.slice(0, 2)}.${d.slice(2)}`;
  if (d.length <= 8) return `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5)}`;
  if (d.length <= 12)
    return `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5, 8)}/${d.slice(8)}`;
  return `${d.slice(0, 2)}.${d.slice(2, 5)}.${d.slice(5, 8)}/${d.slice(
    8,
    12
  )}-${d.slice(12)}`;
}

function aplicarMascaraCpfCnpj(valor) {
  const d = limparNumero(valor);
  return d.length <= 11 ? aplicarMascaraCpf(d) : aplicarMascaraCnpj(d);
}

function onCpfCnpjInput(e) {
  form.cpfCnpj = aplicarMascaraCpfCnpj(e.target.value);
  mensagemErro.value = "";
}

const mensagemErro = ref("");
const cepErro = ref("");
const cepLoading = ref(false);
const inputsErro = ref(false);

function limparCep(valor) {
  return (valor || "").replace(/\D/g, "");
}

function aplicarMascaraCep(valor) {
  const digits = limparCep(valor).slice(0, 8);
  if (digits.length <= 5) return digits;
  return `${digits.slice(0, 5)}-${digits.slice(5)}`;
}

function isCepValido(cepLimpo) {
  return /^\d{8}$/.test(cepLimpo);
}

function onCepInput(e) {
  form.cep = aplicarMascaraCep(e.target.value);
  cepErro.value = "";
}

async function searchCep() {
  const cepLimpo = limparCep(form.cep);

  if (!cepLimpo) {
    cepErro.value = "Informe o CEP.";
    return;
  }
  if (!isCepValido(cepLimpo)) {
    cepErro.value = "CEP inválido. Use o formato 99999-999.";
    return;
  }

  cepErro.value = "";
  cepLoading.value = true;

  try {
    const resp = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
    if (!resp.ok) throw new Error("Falha ao consultar CEP");
    const data = await resp.json();

    if (data.erro) {
      cepErro.value = "CEP não encontrado.";
      return;
    }

    form.rua = data.logradouro || form.rua;
    form.bairro = data.bairro || form.bairro;
    form.cidade = data.localidade || form.cidade;
    form.estado = data.uf || form.estado;
  } catch (e) {
    cepErro.value = "Não foi possível buscar o endereço. Tente novamente.";
  } finally {
    cepLoading.value = false;
  }
}

const telefoneErro = ref("");

function validarTelefone() {
  if (!isTelefoneValido(form.telefone)) {
    telefoneErro.value = "Telefone inválido. Use DDD + número.";
  } else {
    telefoneErro.value = "";
  }
}

const cpfCnpjErro = ref("");

function validarCpfCnpj() {
  if (!isCpfCnpjValido(form.cpfCnpj)) {
    cpfCnpjErro.value = "CPF ou CNPJ inválido.";
  } else {
    cpfCnpjErro.value = "";
  }
}

function submitForm() {
  const camposObrigatorios = [
    "nome",
    "telefone",
    "cep",
    "rua",
    "numero",
    "bairro",
    "cidade",
    "estado",
    "cpfCnpj",
    "obs",
  ];

  const cepLimpo = limparCep(form.cep);
  if (!isCepValido(cepLimpo)) {
    cepErro.value = "CEP inválido. Use o formato 99999-999.";
  }

  const campoVazio = camposObrigatorios.find(
    (campo) => !String(form[campo] || "").trim()
  );

  if (!isTelefoneValido(form.telefone)) {
    telefoneErro.value = "Telefone inválido. Use DDD + número.";
  }

  if (!isCpfCnpjValido(form.cpfCnpj)) {
    cpfCnpjErro.value = "CPF ou CNPJ inválido.";
  }

  if (campoVazio) {
    mensagemErro.value = "Por favor, preencha todos os campos obrigatórios*";
  }

  if (
    !isTelefoneValido(form.telefone) ||
    !isCpfCnpjValido(form.cpfCnpj) ||
    campoVazio ||
    !isCepValido(cepLimpo)
  ) {
    inputsErro.value = true;
    return;
  }

  mensagemErro.value = "";

  localStorage.setItem("formEntrega", JSON.stringify(form));

  window.location.href = "/pagamento";
}
</script>
