<script>
	import { app, page_state } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';

	let { item, small = false } = $props();

	let like = $state(app.likes.includes(item.key));

	const submit = async () => {
		like = !like;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/like`, {
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
			if (app.likes.includes(item.key)) {
				app.likes = app.likes.filter((x) => x !== item.key);
			} else {
				app.likes.push(item.key);
			}
			page_state.clear('save');
		} else {
			like = app.likes.includes(item.key);
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
	<Icon
		icon="heart"
		--icon-fill={like ? 'red' : 'none'}
		--icon-stroke={like ? 'none' : 'var(--ft2)'}
	/>
</Button>
