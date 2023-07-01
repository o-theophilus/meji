<script>
	import { goto } from '$app/navigation';

	import { import.meta.env.VITE_BACKEND } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/comp/button.svelte';

	export let item;

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}ads/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(item)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				item = resp.data.item;
			} else {
				new Error(resp.message);
			}
		}
	};

	let areas = ['home', 'page'];
</script>

<section
	class="item"
	on:click={() => {
		goto(`/${item.alias}`);
	}}
>
	<div class="img">
		<img src={item.photos.length > 0 ? item.photos[0] : '/image/item.png'} alt={item.name} />
	</div>
	<div class="right">
		{item.name}
		<div class="buttons" on:click|stopPropagation>
			{#each areas as area}
				<label class="button">
					{area}
					<input type="checkbox" bind:group={item.placement} value={area} />
				</label>
			{/each}
			<Button
				class="tiny primary"
				name="Submit"
				on:click={() => {
					submit();
				}}
			/>
		</div>
	</div>
</section>

<style>
	.item {
		display: flex;
		gap: var(--gap2);

		height: 100%;

		background: var(--foreground);
		border-radius: var(--brad1);
		border: 2px solid var(--background);
		overflow: hidden;

		cursor: pointer;
		transition: var(--trans1);
	}
	.item:hover {
		border-color: var(--midtone);
	}

	img {
		height: 100px;
	}

	.right {
		display: flex;
		flex-direction: column;
		justify-content: space-around;
	}

	.buttons {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		gap: var(--gap1);
	}
	@media screen and (min-width: 500px) {
	}
</style>
