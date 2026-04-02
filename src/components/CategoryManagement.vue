<template>
  <div class="category-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>商品分类管理</span>
          <el-button type="primary" @click="handleAdd(null)">添加顶级分类</el-button>
        </div>
      </template>

      <el-table
        :data="categoryTree"
        row-key="id"
        border
        v-loading="loading"
        default-expand-all
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
      >
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="sort" label="排序" width="100" />
        <el-table-column prop="isShow" label="是否显示" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.isShow" :active-value="1" :inactive-value="0" @change="handleStatusChange(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250">
          <template #default="{ row }">
            <el-button size="small" type="primary" text @click="handleAdd(row)">添加子分类</el-button>
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const categoryTree = ref([])
const loading = ref(false)

const buildTree = (data, pid = 0) => {
  const tree = []
  data.forEach(item => {
    if (item.pid === pid) {
      const children = buildTree(data, item.id)
      if (children.length > 0) {
        item.children = children
      }
      tree.push(item)
    }
  })
  return tree
}

const fetchCategories = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/store/category/list?group=2') // group 2 for products
    if (res.data.code === 200) {
      categoryTree.value = buildTree(res.data.data, 0)
    }
  } catch (error) {
    ElMessage.error('获取分类失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = (parent) => {
  ElMessage.info('暂未实现表单弹窗')
}

const handleEdit = (row) => {
  ElMessage.info('暂未实现表单弹窗')
}

const handleStatusChange = async (row) => {
  try {
    await axios.post('/api/admin/store/category/save', row)
    ElMessage.success('状态更新成功')
  } catch (error) {
    row.isShow = row.isShow === 1 ? 0 : 1
    ElMessage.error('状态更新失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除此分类吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      const res = await axios.delete(`/api/admin/store/category/delete/${id}`)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        fetchCategories()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
