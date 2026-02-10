<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { Button, RoundButton } from '$lib/button';

	let { ops } = $props();
	let files = $derived(ops.files);

	const order = (dir = true) => {
		ops.error = {};

		if (files.length < 2 || !ops.active) return;
		const currentIndex = files.indexOf(ops.active);

		if (currentIndex == -1) return;
		const newIndex = dir ? currentIndex + 1 : currentIndex - 1;
		if (newIndex < 0 || newIndex >= files.length) return;

		files = files.map((file, i) => {
			if (i === currentIndex) return files[newIndex];
			if (i === newIndex) return files[currentIndex];
			return file;
		});
	};

	const remove = () => {
		ops.error = {};

		let i = files.findIndex((x) => x == ops.active);
		files = files.filter((x) => x != ops.active);

		if (i == 0) {
			ops.active = files[0];
		} else if (i == files.length) {
			ops.active = files[i - 1];
		} else {
			ops.active = files[i];
		}

		if (files.length == 0) {
			ops.active = '/no_photo.png';
		}
	};

	const submit = async () => {
		ops.error = {};

		loading.open('Saving . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/file/${ops.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ files })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			ops.files = resp.item.files;
			module.value.update(resp.item);
			notify.open('Order Saved');
		} else {
			ops.error = resp;
		}
	};
</script>

<div class="line">
	{#each files as x, i (x)}
		<img
			src="{x}/200"
			alt={ops.name}
			class:active={ops.active == x}
			onclick={() => {
				ops.error = {};
				ops.active = x;
			}}
			onerror={(e) => (e.target.src = '/no_photo.png')}
			animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
			role="presentation"
		/>
	{/each}
</div>

<div class="line">
	<RoundButton
		icon="chevron-left"
		disabled={files.length <= 1 || files[0] == ops.active}
		onclick={() => {
			order(false);
		}}
	/>

	<RoundButton
		icon="chevron-right"
		disabled={files.length <= 1 || files[files.length - 1] == ops.active}
		onclick={order}
	/>

	<RoundButton icon="trash-2" disabled={files.length == 0} onclick={remove} />
</div>

<br />

<div class="line">
	<Button
		icon="save"
		disabled={JSON.stringify(ops.files) == JSON.stringify(files)}
		onclick={submit}
	>
		Save
	</Button>

	<Button
		icon="history"
		onclick={() => {
			ops.error = {};
			files = ops.files;
			if (!files.includes(ops.active)) ops.active = files[0];
		}}
		disabled={JSON.stringify(ops.files) == JSON.stringify(files)}
	>
		Reset
	</Button>
</div>

<style>
	.line {
		--size: 50px;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		margin-top: 16px;
	}

	img {
		width: var(--size);
		height: var(--size);
		border-radius: 4px;
		cursor: pointer;

		background-color: var(--bg1);
		outline: 2px solid transparent;
		transition:
			outline-color 0.2s ease-in-out,
			transform 0.2s ease-in-out;
	}

	img:hover {
		outline-color: var(--cl1);
	}

	img.active {
		outline-color: var(--cl1);
		transform: scale(1.1);
	}
</style>
