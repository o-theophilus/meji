<script>
	import { quadIn, quadInOut } from 'svelte/easing';
	import { scale } from 'svelte/transition';
	import { app, page_state } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	let { item, small = false } = $props();

	let like = $derived(app.likes.includes(item.key));

	const submit = async () => {
		let init = [...app.likes];
		if (app.likes.includes(item.key)) {
			app.likes = app.likes.filter((x) => x != item.key);
		} else {
			app.likes.push(item.key);
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/like`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({
				entity_key: item.key,
				entity_type: 'item',
				reaction: 'like'
			})
		});
		resp = await resp.json();

		if (resp.status == 200) {
			app.likes = resp.likes;
			page_state.clear('save');
		} else {
			if (init.includes(item.key)) {
				app.likes.push(item.key);
			} else {
				app.likes = app.likes.filter((x) => x != item.key);
			}
		}
	};
</script>

<Button
	onclick={submit}
	--button-width={small ? '32px' : ''}
	--button-height={small ? '32px' : ''}
	--button-background-color={small ? 'white' : ''}
	--button-background-color-hover={small ? 'hsl(0, 0%, 85%)' : ''}
	--button-outline-color={small ? 'transparent' : ''}
>
	<div class="block">
		<Icon icon="heart" --icon-stroke="none" />
		{#key like}
			<div class="count" transition:scale={{ easing: quadInOut }}>
				<Icon
					icon="heart"
					--icon-fill={like ? 'red' : 'none'}
					--icon-stroke={like ? 'none' : 'var(--ft2)'}
				/>
			</div>
		{/key}
	</div>
</Button>

<style>
	div {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.block {
		position: relative;
	}

	.block div {
		position: absolute;
	}
</style>
