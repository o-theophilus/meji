<script>
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Ads from './ads.form.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
	let src = $derived(item.files[0] || '/no_photo.png');
</script>

<div class="img">
	<img {src} alt={item.name} onerror={() => (src = '/no_photo.png')} />
	{#if app.user.access.includes('item:edit_file') && edit_mode}
		<div class="edit line">
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

			<Edit_Button
				onclick={() => {
					module.open(Ads, {
						key: item.key,
						name: item.name,
						files: item.files
					});
				}}
			>
				Edit Ads
			</Edit_Button>
		</div>
	{/if}
</div>

{#if item.files.length > 1}
	<div class="line">
		{#each item.files as x}
			<img
				src="{x}/200"
				alt={item.name}
				class:active={src == x}
				onclick={() => (src = x)}
				onerror={(e) => (e.target.src = '/no_photo.png')}
				role="presentation"
			/>
		{/each}
	</div>
{/if}

<style>
	.img {
		position: relative;
		background-color: var(--bg1);
		border-radius: 8px;
		overflow: hidden;

		& img {
			display: block;

			width: 100%;
			aspect-ratio: 1;
			object-fit: cover;
		}

		& .edit {
			position: absolute;
			bottom: 8px;
			left: 8px;
		}
	}

	.line {
		--size: 40px;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		margin-top: 16px;

		& img {
			width: var(--size);
			height: var(--size);
			border-radius: 4px;
			cursor: pointer;

			background-color: var(--bg1);
			outline: 2px solid transparent;
			transition:
				outline-color 0.2s ease-in-out,
				transform 0.2s ease-in-out;

			&:hover {
				outline-color: var(--cl1);
			}

			&.active {
				outline-color: var(--cl1);
				transform: scale(1.1);
			}
		}
	}
</style>
