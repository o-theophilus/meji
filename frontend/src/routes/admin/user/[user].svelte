<script context="module">
	import { loading } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	export async function load({ fetch, session, params }) {
		loading.set(true);
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user/${params.user}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: session.token
			}
		});

		if (_resp.ok) {
			loading.set(false);
			let resp = await _resp.json();

			if (resp.status == 200) {
				return {
					props: {
						user: resp.data.user
					}
				};
			} else {
				return {
					status: 404,
					error: resp.message
				};
			}
		}
	}
</script>

<script>
	import User from '$lib/user/index.svelte';
	import { _tick, user, module } from '$lib/store.js';

	import Role from './_role_form.svelte';

	export let user;
	$: if ($_tick) {
		user = $_tick;
		$_tick = '';
	}
</script>

<svelte:head>
	<title>{user.name} | Meji</title>
</svelte:head>

<User {user}>
	{#if $user?.roles.includes('admin')}
		<Button
			class="wide"
			name="Set Role"
			on:click={() => {
				$module = {
					module: Role,
					data: {
						user
					}
				};
			}}
		/>
	{/if}
</User>
