<script context="module">
	export async function load({ session, url }) {
		if (session.user.login) {
			return {
				props: {
					user: session.user
				}
			};
		}

		return {
			status: 302,
			redirect: `/?module=login&return_url=${url.pathname}`
		};
	}
</script>

<script>
	import { user, _tick, currency } from '$lib/store.js';

	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	import Signout from './_signout.svelte';
	import User from '$lib/user/index.svelte';

	export let user;
	$: user = $user ? $user : user;

	$: if ($_tick) {
		$user = $_tick;
		$_tick = '';
	}
</script>

<svelte:head>
	<title>{user.name} | Meji</title>
</svelte:head>

<User {user}>
	<Body>
		<div>
			<Button
				class="tertiary"
				name="Account Balance: {currency(user.acc_balance)}"
				href="account/balance"
			/>
		</div>
	</Body>
	<Body>
		<Button class="wide" name="Orders" href="/order" />
		<!-- <Button name="* Activity" href="/account/activity" /> -->
	</Body>
	<Body>
		<Signout let:submit>
			<Button class="wide" name="SIGN OUT" on:click={submit} />
		</Signout>
	</Body>

	{#if user.roles.includes('admin')}
		<Body>
			<Button class="wide" name="Admin" href="/admin" />
		</Body>
	{/if}
</User>>

<style>
</style>
