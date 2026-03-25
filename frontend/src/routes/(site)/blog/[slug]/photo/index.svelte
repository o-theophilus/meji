<script>
	import { app, module } from '$lib/store.svelte.js';

	import Button from '../button.svelte';
	import Edit from './edit.svelte';

	let { blog, edit_mode, update } = $props();
	let src = $derived(blog.photo || '/no_photo.png');
</script>

<div class="img">
	<img {src} alt={blog.title} onerror={() => (src = '/file_error.png')} />
	<div class="line">
		{#if app.user.access.includes('blog.edit_photo') && edit_mode}
			<Button
				onclick={() => {
					module.open(Edit, {
						key: blog.key,
						name: blog.title,
						photo: blog.photo,
						type: 'blog',
						slug: `/blogs/${blog.key}/photo`,
						update
					});
				}}
			>
				Edit Photo
			</Button>
		{/if}
	</div>
</div>

<style>
	.img {
		position: relative;
	}

	img {
		display: block;

		width: 100%;
		border-radius: 8px;

		background-color: var(--bg2);
	}
	.img .line {
		position: absolute;
		bottom: 8px;
		left: 8px;
	}
</style>
