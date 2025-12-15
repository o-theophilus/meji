<script>
	import { module, app } from '$lib/store.svelte.js';

	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
	let src = $derived(item.files[0] || '/no_photo.png');
</script>

<div class="img">
	<img {src} alt={item.name} onerror={() => (src = '/file_error.png')} />
	<div class="edit">
		{#if app.user.access.includes('item:edit_file') && edit_mode}
			<Edit_Button
				onclick={() => {
					module.open(Form, {
						key: item.key,
						name: item.name,
						files: item.files,
						update
					});
				}}
			>
				Edit Files
			</Edit_Button>
		{/if}
	</div>
</div>

{#if item.files.length > 1}
	<div class="line">
		{#each item.files as x}
			<img
				src="{x}/200"
				alt={item.name}
				class:active={src == x}
				onclick={() => (src = x)}
				onerror={(e) => (e.target.src = '/file_error.png')}
				role="presentation"
			/>
		{/each}
	</div>
{/if}

<style>
	.img {
		position: relative;
	}

	img {
		display: block;

		width: 100%;
		border-radius: var(--sp1);

		background-color: var(--bg2);
	}
	.edit {
		position: absolute;
		bottom: var(--sp1);
		left: var(--sp1);
	}

	.line {
		--size: 50px;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);
		flex-wrap: wrap;
		margin-top: var(--sp2);
	}

	.line img {
		width: var(--size);
		height: var(--size);
		border-radius: var(--sp0);
		cursor: pointer;

		background-color: var(--bg2);
		outline: 2px solid transparent;
		transition:
			outline-color var(--trans),
			transform var(--trans);
	}

	.line img:hover {
		outline-color: var(--cl1);
	}

	.line img.active {
		outline-color: var(--cl1);
		transform: scale(1.1);
	}
</style>
