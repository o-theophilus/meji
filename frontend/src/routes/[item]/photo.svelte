<script>
	import { module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Photo from './_photo.svelte';

	export let item;
	export let edit_mode = false;

	let index = 0;
</script>

<div class="img">
	<img
		src={item.photos.length > 0 ? item.photos[index] : '/image/item.png'}
		alt={item.name}
		onerror="this.src='/image/item.png'"
	/>
	{#if edit_mode}
		<div class="edit">
			<Button
				icon={item.photos.length == 0 ? 'add' : 'edit'}
				icon_size="12"
				class="tiny"
				on:click={() => {
					$module = {
						module: Photo,
						item
					};
				}}
			/>
		</div>
	{/if}
</div>

{#if item.photos.length > 1}
	<div class="slide">
		{#each item.photos as photo, i}
			<button
				on:click={() => {
					index = i;
				}}
			>
				<img src="{photo}/200" alt={item.name} onerror="this.src='/image/item.png'" />
			</button>
		{/each}
	</div>
{/if}

<style>
	.img {
		position: relative;
		height: auto;
	}
	img {
		border-radius: var(--sp0);
		width: 100%;
	}
	.edit {
		position: absolute;
		bottom: var(--sp2);
		right: var(--sp2);
	}

	.slide {
		display: flex;
		justify-content: center;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
	.slide button {
		border: none;
		background-color: transparent;
	}
	.slide img {
		--size: 50px;
		width: var(--size);
		height: var(--size);
		cursor: pointer;

		border: 2px solid var(--ac5);
		border-radius: var(--sp0);
		object-fit: cover;

		transition: var(--trans1);
	}
	.slide img:hover {
		border-color: var(--ac3);
		transform: scale(1.1);
	}
</style>
