<script>
	import { Datetime } from '$lib/macro';
	let { datetime } = $props();
</script>

<hr style="border-color: gray; margin: 24px 0;" />
<b style="font-size: 0.8rem;">Delivery Date:</b>
<br />
<br />

Date:
<Datetime {datetime} type="day_full" />,
<Datetime {datetime} type="date_numeric" /><br />
Time:
<Datetime {datetime} type="time_period" />
