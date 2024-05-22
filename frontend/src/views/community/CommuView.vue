<template>
  <div class="container">
    
    <div class="white">
      <p class="body fs-3 mt-3">자유게시판</p>
      <hr>
    </div>
    <p class="body fs-3 mt-3">인기글</p>
    <table class="table table-dark table-striped table-hover">
      <thead>
        <tr>
          <th style="width: 50px;">분류</th>
          <th>제목</th>
          <th>내용</th>
          <th>작성자</th>
          <th>좋아요❤</th>
          <th>조회수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in topArticles" :key="article.id" @click="goToDetail(article.id)">
          <td>{{ categoryNames[article.category] || '알 수 없음' }}</td>
          <td>{{ article.title }}</td>
          <td>{{ article.content }} ({{ article.comments_count }})</td>
          <td @click.stop="goProfile(article.user.id)">{{ article.user.username }}</td>
          <td>{{ article.likes_count }}</td>
          <td>{{ article.click_count }}</td>
        </tr>
      </tbody>
    </table>
  <!-- 글쓰기 -->
    <div class="white">
      <p class="body fs-3 mt-4">게시글</p>
      <hr>
    </div>
    <table class="table table-dark table-striped table-hover">
      <thead>
      <tr>
        <th style="width: 50px;">분류</th>
        <th>제목</th>
        <th>내용</th>
        <th>작성자</th>
        <th>좋아요❤</th>
        <th>조회수</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="article in paginatedArticles" :key="article.id" @click="goToDetail(article.id)">
          <td>{{ categoryNames[article.category] || '알 수 없음' }}</td>
          <td>{{ article.title }}</td>
          <td>{{ article.content }} ({{ article.comments_count }})</td>
          <td @click.stop="goProfile(article.user.id)">{{ article.user.username }}</td>
          <td>{{ article.likes_count}}</td>
          <td>{{ article.click_count }}</td>
        </tr>
      </tbody>
    </table> 

    <!-- 페이지 네비게이션 -->
    <div class="d-flex justify-content-between">
      <div class="d-flex justify-content-center align-items-center" style="flex-grow: 1;">
        <nav aria-label="Page navigation example">
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="" @click.prevent="prevPage">Previous</a>
            </li>
            <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: page === currentPage }">
              <a class="page-link" href="" @click.prevent="goToPage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" href="" @click.prevent="nextPage">Next</a>
            </li>
          </ul>
        </nav>
      </div>
      <!-- 글쓰기 버튼 컨테이너 -->
      <div>
        <button class="btn btn-primary btn-mg" @click="router.push({name: 'create'})">새 글작성</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useArticleStore } from '@/stores/articleStore';

const store = useArticleStore();
const router = useRouter();
const category = ref(null);
const currentPage = ref(1);
const postsPerPage = 10;

const categoryNames = {
  1: '영화',
  2: '배우',
  3: '잡담'
};

onMounted(async () => {
  await store.getArticles();
  if (store.articles.posts.length > 0) {
    category.value = categoryNames[store.articles.posts[0].category] || '알 수 없음';
  } else {
    category.value = 'No Category';
  }
});

const goProfile = (user_id) => {
  router.push({name: 'profile', params: { id: user_id}})
}

const goToDetail = (id) => {
  router.push({ name: 'articleDetail', params: { id } });
};


// 최근 하루의 글 중 좋아요가 많은 상위 3개 글
const topArticles = computed(() => {
  const oneDayAgo = new Date();
  oneDayAgo.setDate(oneDayAgo.getDate() - 1);
  
  // store.articles.posts가 존재하는지 확인
  if (!store.articles.posts || !Array.isArray(store.articles.posts)) {
    return [];
  }

  return store.articles.posts
    .filter(article => new Date(article.created_at) > oneDayAgo)
    .sort((a, b) => b.likes_count - a.likes_count || b.click_count - a.click_count)
    .slice(0, 3);
});

// 페이지 당 10개의 글
const paginatedArticles = computed(() => {
  // store.articles.posts가 배열인지 확인합니다.
  // 배열이 아니면 빈 배열을 반환합니다.
  if (!Array.isArray(store.articles.posts)) {
    return [];
  }
  
  const currentPageNumber = Number.isInteger(currentPage.value) ? currentPage.value : 1;
  const postsPerPageNumber = Number.isInteger(postsPerPage) ? postsPerPage : 10;
  
  const reversedPosts = [...store.articles.posts].reverse();
  
  const start = (currentPageNumber - 1) * postsPerPageNumber;
  const end = start + postsPerPageNumber;
  
  return reversedPosts.slice(start, end);
});

const totalPages = computed(() => {
  // store.articles.posts가 배열인지, 그리고 정의되어 있는지 체크
  if (!Array.isArray(store.articles.posts)) {
    return 0; // 배열이 아니면 0 페이지를 반환
  }
  return Math.ceil(store.articles.posts.length / postsPerPage);
});

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const goToPage = (page) => {
  currentPage.value = page;
};
</script>




<style scoped>
.body {
  color: #ffffff;
}

hr {
  border-top-color: #ffffff; /* 흰색으로 변경 */
}

</style>
