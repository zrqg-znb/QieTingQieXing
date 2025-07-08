import request from '@/utils/request'

// 文章相关接口
export const getArticles = (params) => {
  return request({
    url: '/api/blog/articles/',
    method: 'get',
    params
  })
}

export const getArticle = (id) => {
  return request({
    url: `/api/blog/articles/${id}/`,
    method: 'get'
  })
}

export const createArticle = (data) => {
  return request({
    url: '/api/blog/articles/',
    method: 'post',
    data
  })
}

export const updateArticle = (id, data) => {
  return request({
    url: `/api/blog/articles/${id}/`,
    method: 'put',
    data
  })
}

export const deleteArticle = (id) => {
  return request({
    url: `/api/blog/articles/${id}/`,
    method: 'delete'
  })
}

export const likeArticle = (id) => {
  return request({
    url: `/api/blog/articles/${id}/like/`,
    method: 'post'
  })
}

export const unlikeArticle = (id) => {
  return request({
    url: `/api/blog/articles/${id}/unlike/`,
    method: 'post'
  })
}

// 分类相关接口
export const getCategories = () => {
  return request({
    url: '/api/blog/categories/',
    method: 'get'
  })
}

export const createCategory = (data) => {
  return request({
    url: '/api/blog/categories/',
    method: 'post',
    data
  })
}

export const updateCategory = (id, data) => {
  return request({
    url: `/api/blog/categories/${id}/`,
    method: 'put',
    data
  })
}

export const deleteCategory = (id) => {
  return request({
    url: `/api/blog/categories/${id}/`,
    method: 'delete'
  })
}

// 标签相关接口
export const getTags = () => {
  return request({
    url: '/api/blog/tags/',
    method: 'get'
  })
}

export const createTag = (data) => {
  return request({
    url: '/api/blog/tags/',
    method: 'post',
    data
  })
}

export const updateTag = (id, data) => {
  return request({
    url: `/api/blog/tags/${id}/`,
    method: 'put',
    data
  })
}

export const deleteTag = (id) => {
  return request({
    url: `/api/blog/tags/${id}/`,
    method: 'delete'
  })
}

// 评论相关接口
export const getComments = (articleId) => {
  return request({
    url: `/api/blog/articles/${articleId}/comments/`,
    method: 'get'
  })
}

export const createComment = (articleId, data) => {
  return request({
    url: `/api/blog/articles/${articleId}/comments/`,
    method: 'post',
    data
  })
}

export const updateComment = (articleId, commentId, data) => {
  return request({
    url: `/api/blog/articles/${articleId}/comments/${commentId}/`,
    method: 'put',
    data
  })
}

export const deleteComment = (articleId, commentId) => {
  return request({
    url: `/api/blog/articles/${articleId}/comments/${commentId}/`,
    method: 'delete'
  })
}

export const likeComment = (articleId, commentId) => {
  return request({
    url: `/api/blog/articles/${articleId}/comments/${commentId}/like/`,
    method: 'post'
  })
}

export const unlikeComment = (articleId, commentId) => {
  return request({
    url: `/api/blog/articles/${articleId}/comments/${commentId}/unlike/`,
    method: 'post'
  })
}