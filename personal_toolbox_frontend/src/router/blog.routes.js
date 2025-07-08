import ArticleList from '@/views/blog/ArticleList.vue'
import ArticleDetail from '@/views/blog/ArticleDetail.vue'
import ArticleEditor from '@/views/blog/ArticleEditor.vue'

export default [
  {
    path: 'blog',
    children: [
      {
        path: 'articles',
        name: 'ArticleList',
        component: ArticleList,
        meta: {
          title: '文章列表'
        }
      },
      {
        path: 'article/new',
        name: 'CreateArticle',
        component: ArticleEditor,
        meta: {
          title: '写文章',
          requiresAuth: true
        }
      },
      {
        path: 'article/:id',
        name: 'ArticleDetail',
        component: ArticleDetail,
        meta: {
          title: '文章详情'
        }
      },
      {
        path: 'article/:id/edit',
        name: 'EditArticle',
        component: ArticleEditor,
        meta: {
          title: '编辑文章',
          requiresAuth: true
        }
      }
    ]
  }
]