<script setup lang="ts">
import { ref } from "vue";

interface AIResult {
  sentiment: string;
  category: string;
  reply: string;
}

interface ResponseData {
  success?: boolean;
  message?: string;
  ai_analysis?: AIResult;
  detail?: any;
}

const form = ref({
  name: "",
  email: "",
  phone: "",
  comment: "",
});

const loading = ref(false);

const result = ref<ResponseData | null>(null);

const errorMessage = ref("");

async function sendForm() {
  loading.value = true;

  result.value = null;

  errorMessage.value = "";

  try {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/api/contact`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(form.value),
      },
    );

    const data = await response.json();

    if (!response.ok) {
      if (Array.isArray(data.detail)) {
        errorMessage.value = data.detail
          .map((error: any) => error.msg)
          .join(", ");
      } else {
        errorMessage.value = data.detail || "Ошибка отправки формы";
      }

      return;
    }

    result.value = data;

    form.value = {
      name: "",
      email: "",
      phone: "",
      comment: "",
    };
  } catch {
    errorMessage.value = "Сервер недоступен. Попробуйте позже.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main class="page">
    <div class="container">
      <div class="header">
        <h1>Contact developer</h1>

        <p class="subtitle">
          Оставьте заявку — AI проанализирует обращение и подготовит ответ.
        </p>
      </div>

      <form @submit.prevent="sendForm">
        <input v-model="form.name" placeholder="Ваше имя" required />

        <input v-model="form.email" placeholder="Email" type="email" required />

        <input v-model="form.phone" placeholder="Телефон" required />

        <textarea
          v-model="form.comment"
          placeholder="Расскажите о задаче..."
          required
        />

        <button :disabled="loading">
          <span v-if="loading"> Отправка... </span>

          <span v-else> Отправить заявку </span>
        </button>
      </form>

      <transition name="fade">
        <div v-if="errorMessage" class="error">
          <h3>❌ Ошибка</h3>

          <p>
            {{ errorMessage }}
          </p>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="result" class="success">
          <h3>Заявка отправлена</h3>

          <p>
            {{ result.message }}
          </p>

          <div v-if="result.ai_analysis" class="ai-card">
            <h4>AI Analysis</h4>

            <div class="ai-row">
              <span> Sentiment </span>

              <strong>
                {{ result.ai_analysis.sentiment }}
              </strong>
            </div>

            <div class="ai-row">
              <span> Category </span>

              <strong>
                {{ result.ai_analysis.category }}
              </strong>
            </div>

            <p class="ai-title">AI reply:</p>

            <blockquote>
              {{ result.ai_analysis.reply }}
            </blockquote>
          </div>
        </div>
      </transition>
    </div>
  </main>
</template>
