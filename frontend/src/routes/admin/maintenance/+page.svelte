<script>
	import { Button } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import { app, loading, notify } from '$lib/store.svelte.js';

	const cron = async (endpoint, msg, method = 'post') => {
		loading.open('Running maintenance...');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}${endpoint}`, {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			}
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			notify.open(msg);
		} else {
			error = result;
		}
	};
</script>

<Meta title="Maintenance" />
<Log entity_type={'page'} />

<Content>
	<div class="page_title">Maintenance</div>

	<br />
	<Button onclick={() => cron('/cron', 'Cron executed successfully', 'get')} size="wide">
		1-click Maintenance
	</Button>
	<br /><br />
	<Button onclick={() => cron('/maintenance/session', 'Expired sessions cleaned up')} size="wide">
		Clean up expired sessions
	</Button>
	<br /><br />
	<Button onclick={() => cron('/maintenance/anonymous', 'Anonymous users cleaned up')} size="wide">
		Clean up anonymous users
	</Button>
	<br /><br />
	<Button onclick={() => cron('/maintenance/coupon', 'Coupons expired')} size="wide">
		Expire coupon
	</Button>
</Content>

<style>
</style>
